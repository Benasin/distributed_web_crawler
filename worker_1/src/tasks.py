import requests
from bs4 import BeautifulSoup
from celery_config import app
from sqlalchemy import create_engine, Column, String, Text, Integer, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker # type: ignore

Base = declarative_base()
engine = create_engine('postgresql://newsuser:password@db:5432/newsdb')
Session = sessionmaker(bind=engine)
session = Session()

class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    title = Column(String)
    content = Column(Text)

Base.metadata.create_all(engine)

@app.task
def fetch_news(url, site):
    try:
        response = requests.get(url)
        response.raise_for_status()
        page_content = response.content
        soup = BeautifulSoup(page_content, 'html.parser')

        if site == 'vnexpress':
            # Extract the news content based on HTML structure
            title_elements = soup.find_all(class_='title-news')
            links = [title.find('a').get('href') for title in title_elements]
            titles = [title.get_text().strip() for title in title_elements]
            description_elements = soup.find_all(class_='description')
            descriptions = [description.get_text().strip() for description in description_elements]
        elif site == 'kinhtedothi':
            # Extract the news content based on HTML structure
            title_elements = soup.find_all(class_='story__title')
            links = ['https://kinhtedothi.vn' + title.find('a').get('href') for title in title_elements]
            titles = [title.get_text().strip() for title in title_elements]
            description_elements = soup.find_all(class_='story__summary')
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
