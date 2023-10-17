from typing import Union

import datetime
import json
import re
from datetime import timedelta

import requests
from src.core import settings
import googleapiclient.discovery
from pytube import Search


async def get_video_url(url: str) -> (str, str):
    # Regular expression to match YouTube video ID
    pattern = r"(?:https://)?(?:www\.)?(?:youtube\.com|youtu\.be)/(?:watch\?v=)?(.{11})"
    match = re.search(pattern, url)
    if match:
        return f"https://www.youtube.com/watch?v={match.group(1)}", match.group(1)
    else:
        return None, None


async def get_video_information(
    video_id: str,
) -> (timedelta, list[str], str, str):
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=settings.YOUTUBE_API_KEY
    )
    request = youtube.videos().list(part="snippet, statistics", id=video_id)
    response = request.execute()

    return (
        datetime.datetime.now()
        - datetime.datetime.fromisoformat(
            response["items"][0]["snippet"]["publishedAt"][:-1]
        ),
        response["items"][0]["snippet"]["tags"]
        if "tags" in response["items"][0]["snippet"].keys()
        else [],
        response["items"][0]["snippet"]["title"],
        response["items"][0]["snippet"]["description"],
        response["items"][0]["statistics"]["viewCount"],
    )


async def get_channel_id(video_id: str) -> Union[str, None]:
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=settings.YOUTUBE_API_KEY
    )

    response = youtube.videos().list(part="snippet", id=video_id).execute()

    try:
        channel_id = response["items"][0]["snippet"]["channelId"]
    except IndexError as ex:
        return None

    return channel_id


async def get_channel_information(channel_id: str) -> (timedelta, int):
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=settings.YOUTUBE_API_KEY
    )

    response = (
        youtube.channels().list(part="snippet, statistics", id=channel_id).execute()
    )

    return datetime.datetime.now() - datetime.datetime.fromisoformat(
        response["items"][0]["snippet"]["publishedAt"][:-1]
    ), int(response["items"][0]["statistics"]["subscriberCount"])


async def get_video_seo(tags: list[str], title: str, description: str) -> float:
    tags_position = create_tag_position_list(tags, title)
    headers = {
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 OPR/81.0.4196.61",
    }
    payload = {
        "client": "3.65.0",
        "country": "US",
        "description": str(description.encode("ascii", errors="ignore")),
        "language": "en",
        "tags": tags_position,
        "title": str(title.encode("ascii", errors="ignore")),
    }
    result = requests.post(
        "https://app.vidiq.com/v2/youtube_seo_score",
        headers=headers,
        data=json.dumps(payload),
    )
    return float(json.loads(result.text)["overall"])


def create_tag_position_list(keywords: list[str], video_title: str) -> dict[str:int]:
    tags_position = []
    for key in keywords:
        tag_info = {"text": key}
        search_result = search(key)
        if video_title in search_result:
            tag_info["search_rank"] = search_result.index(video_title) + 1

        tags_position.append(tag_info)
    return tags_position


def search(query) -> list:
    search_result = Search(query.encode())
    return [video.title for video in search_result.results]
