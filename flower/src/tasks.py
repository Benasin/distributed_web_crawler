import requests
from bs4 import BeautifulSoup
from celery_config import app
from sqlalchemy import create_engine, Column, String, Text, Integer, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker # type: ignore

Base = declarative_base()
engine = create_engine('postgresql://main_newsuser:main_password@main_db:5432/main_newsdb')
Session = sessionmaker(bind=engine)
session = Session()

class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    title = Column(String)
    content = Column(Text)

Base.metadata.create_all(engine)

def extract_link(title_element, site):
  link = title_element.find('a')
  if link is None:
    link = title_element
  link = link.get("href")
  if link[0] == "/" or link[0] == ".":
    link = site + link
  return link

@app.task
def fetch_news(url, site, title_tag, description_tag):
    try:
        response = requests.get(url)
        response.raise_for_status()
        page_content = response.content
        soup = BeautifulSoup(page_content, 'html.parser')

        # Extract the news content based on HTML structure
        title_elements = soup.find_all(class_=title_tag)
        links = [extract_link(title, site) for title in title_elements]
        titles = [title.get_text().strip() for title in title_elements]
        description_elements = soup.find_all(class_=description_tag)
        descriptions = [description.get_text().strip() for description in description_elements]

        articles = [{'title': title, 'link': link, 'description': description} for title, link, description in zip(titles, links, descriptions)]

        for article in articles:
            news = News(url=article['link'], title=article['title'], content=article['description'])
            session.add(news)
            session.commit()
        
        return {'url': url, 'status': 'success'}
    except requests.RequestException as e:
        return {'url': url, 'error': str(e)}
    except exc.IntegrityError:
        session.rollback()
        return {'url': url, 'error': 'Already exists'}
    except Exception as e:
        session.rollback()
        return {'url': url, 'error': str(e)}
