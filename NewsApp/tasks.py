from .models import Category, Post
from celery import shared_task

import requests

count = 20
@shared_task(bind=True)
def test_func(self):
    return "Done"

@shared_task(bind=True)
def get_data_from_hacker_news(self):
    response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json')
    story_ids = response.json()[:count]

    for story_id in story_ids:
        story_response = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json')
        story = story_response.json()
        try:
            category = Category.objects.get(name=story['type'])
        except Category.DoesNotExist:
            category = Category(name=story['type'])
            category.save()

        hacker_news_id = story['id']

        try:
            new_post = Post.objects.get(hacker_news_id=hacker_news_id)
        except Post.DoesNotExist:
            new_post = Post()
            new_post.category = category
            new_post.title = story['title']
            new_post.views = int(story['score'])

            try:
                new_post.content = story['url']
                new_post.posted_by = story['by']
            except:
                pass

            
            new_post.hacker_news_id = hacker_news_id

            new_post.save()

    return "done polling hacker news"