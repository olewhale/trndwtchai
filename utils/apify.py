import os, sys, json
from apify_client import ApifyClient
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pytz

# Загружаем переменные из .env
load_dotenv()

# Convert ISO 8601 to a normal timestamp
#formatted_timestamp = datetime.strptime('2024-10-03T00:22:51.000Z', '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')

# doesn't work yet. it should
def instagram_user_scrapper(request_dict):
    #Script that get count of followers use this apify actor - its free! =)
    #https://console.apify.com/actors/xMBzmb4DgNHnkOn4q/input
    return None


def instagram_posts_scrapper(request_dict, start_of_day, days=3, range_days=None):
    # Загружаем переменные из .env
    load_dotenv()
    # Инициализируем клиента Apify
    APIFY_API = os.getenv('APIFY_API')
    #client = ApifyClient(APIFY_API)
    client = ApifyClient("apify_api_Mh8rUvYzbCNWJJbHyh8okswsRTA39z1cA3BD")


    # Рассчитываем целевые дни
    target_day = datetime.now() - timedelta(days=days)
    start_of_day = target_day.date()  # Получаем только дату
    end_of_day = (target_day + timedelta(days=1)).date()  # Получаем только дату

    # Если указан диапазон дней
    if range_days:
        start_range, end_range = map(int, range_days.split('-'))
        start_of_day = (datetime.now() - timedelta(days=end_range)).date()  # Получаем только дату
        end_of_day = (datetime.now() - timedelta(days=start_range)).date()  # Получаем только дату

    # Извлекаем список username
    usernames = [
        item.get('username') for item in request_dict
        if isinstance(item, dict)
    ]
    
    run_input = {
        "username": usernames,
        "resultsLimit": 40,
        "onlyPostsNewerThan": start_of_day.strftime('%Y-%m-%d'),
        "skipPinnedPosts":
        True  # Или True, если нужно пропускать закрепленные посты
    }
    print("Apify input created: " + str(run_input))
    
    #print("Локальные переменные:", json.dumps(locals(), default=str, ensure_ascii=False, indent=4))
    #sys.exit()

    # Запуск актора и ожидание его завершения
    try:
        run = client.actor("apify/instagram-post-scraper").call(
            run_input=run_input)
        dataset_items = client.dataset(
            run["defaultDatasetId"]).list_items().items
        
        print('--------')
        print('count of input items: ' + str(len(dataset_items)))
        print('-----')

    except Exception as e:
        print(f"Error processing users: {e}")
    #print(reelsData)
    return dataset_items

def tiktok_posts_scrapper(request_dict, start_of_day, days=3, range_days=None):
    # Загружаем переменные из .env
    load_dotenv()
    # Инициализируем клиента Apify
    APIFY_API = os.getenv('APIFY_API')
    #client = ApifyClient(APIFY_API)
    client = ApifyClient("apify_api_Mh8rUvYzbCNWJJbHyh8okswsRTA39z1cA3BD")

    # Извлекаем список username
    usernames = [
        item.get('username') for item in request_dict
        if isinstance(item, dict)
    ]

    '''
    run_input = {
        "excludePinnedPosts": True,
        "oldestPostDate": start_of_day.strftime('%Y-%m-%d'),
        "profiles": usernames,
        "resultsPerPage": 100,
        "shouldDownloadCovers": False,
        "shouldDownloadSlideshowImages": False,
        "shouldDownloadSubtitles": False,
        "shouldDownloadVideos": True,
        "profileScrapeSections": [
            "videos"
        ],
        "profileSorting": "latest",
        "searchSection": "",
        "maxProfilesPerQuery": 10
    }
    '''
    run_input = {
        "maxItems": 5000,
        "until": start_of_day.strftime('%Y-%m-%d'),
        "usernames": usernames
    }


    print("Apify input created: " + str(run_input))
    
    #print("Локальные переменные:", json.dumps(locals(), default=str, ensure_ascii=False, indent=4))
    #sys.exit()

    
    # Запуск актора и ожидание его завершения
    try:
        run = client.actor("apidojo/tiktok-profile-scraper").call(
            run_input=run_input)
        dataset_items = client.dataset(
            run["defaultDatasetId"]).list_items().items
        
        print('--------')
        print('count of input items: ' + str(len(dataset_items)))
        print('-----')

    except Exception as e:
        print(f"Error processing users: {e}")
    #print(reelsData)
    return dataset_items


def reels_scrapper(links):
    # Initialize the ApifyClient with your API token
    client = ApifyClient(os.environ['APIFY_API'])

    print("-------links получены: " + str(links) + "\n")
    #reelslinks = links
    run_input = {
        "addParentData": False,
        "directUrls": links,
        "enhanceUserSearchWithFacebookPage": False,
        "isUserReelFeedURL": False,
        "isUserTaggedFeedURL": False,
        "resultsLimit": 200,
        "resultsType": "posts",
        "searchLimit": 1,
        "searchType": "hashtag"
    }
    print("Apify input created: " + str(run_input))

    reelsData = []
    # Запуск актора и ожидание его завершения
    try:
        run = client.actor("apify/instagram-scraper").call(run_input=run_input)
        raw_data = client.dataset(run["defaultDatasetId"]).list_items().items

        # Фильтрация элементов без ошибки и с исключением типа "slide"
        reelsData = [
            item for item in raw_data
            if 'error' not in item and item.get('type') != 'Sidecar'
        ]

        # Выводим сообщение об ошибках, если они есть
        for item in raw_data:
            if 'error' in item:
                print(
                    f"Error in URL {item['url']}: {item['error']} - {item.get('errorDescription', 'No description')}"
                )
            elif item.get('type') == 'Sidecar':
                print(f"Slide-type Reels found at URL {item['url']}")

    except Exception as e:
        print(f"Error processing users: {e}")
    #print(json.dumps(reelsData, indent=4, ensure_ascii=False))
    return reelsData


def tiktok_scrapper(links):
    # Initialize the ApifyClient with your API token
    client = ApifyClient(os.environ['APIFY_API'])

    print("-------links получены: " + str(links))
    #reelslinks = links
    run_input = {
        "excludePinnedPosts": False,
        "postURLs": links,
        "resultsPerPage": 100,
        "shouldDownloadCovers": False,
        "shouldDownloadSlideshowImages": False,
        "shouldDownloadSubtitles": False,
        "shouldDownloadVideos": True,
        "searchSection": "",
        "maxProfilesPerQuery": 10
    }

    print("Apify input created: " + str(run_input))

    videoData = []
    # Запуск актора и ожидание его завершения
    try:
        run = client.actor("clockworks/free-tiktok-scraper").call(
            run_input=run_input)
        raw_data = client.dataset(run["defaultDatasetId"]).list_items().items

    except Exception as e:
        print(f"Error processing users: {e}")
    #print(json.dumps(reelsData, indent=4, ensure_ascii=False))
    return raw_data


def instagram_scrapper_filter_sorter(dataset_items, request_dict, start_of_day, end_of_day):
    reelsData = []
    # Фильтруем только рилсы (type='Video'), которые попадают в целевые сутки (позавчера)
    for item in dataset_items:
        if 'type' in item and item['type'] == 'Video':
            # Парсим время публикации
            post_time = datetime.strptime(item['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ").date()  # Получаем только дату
            #print(post_time)
            # Проверяем, входит ли пост в диапазон целевых дат
            if start_of_day <= post_time <= end_of_day:
                reelsData.append(item)
    # Преобразуем request_dict в словарь для быстрого поиска, у меня тут появляется такой массив {'username_1': 2000, 'username_2':34000}
    username_limits = {
        entry['username']: entry['viewsFilter']
        for entry in request_dict
    }

    # Фильтруем рилсы
    filtered_reels = [
        reel for reel in reelsData
        if (reel['inputUrl'].split('/')[-1] in username_limits and 
            reel.get('videoPlayCount') is not None and  # Проверка на None
            reel.get('videoPlayCount', 0) >= username_limits[reel['inputUrl'].split('/')[-1]])
    ]

    # CUSTOM FILTER
    # filtered_reels = [
    #     reel for reel in reelsData
    #     if (reel['inputUrl'].split('/')[-1] in username_limits and 
    #         reel.get('videoPlayCount') is not None and  # Проверка на None
    #         reel.get('videoPlayCount', 0) >= 10000 and reel.get('videoPlayCount', 0) < 30000)
    # ]

    # Сортировка только по 'timestamp'
    sorted_data = sorted(
        filtered_reels,
        key=lambda x: (
            x.get('timestamp', 0)  # Используем 0 в качестве значения по умолчанию для timestamp, если он отсутствует
        )
    )

    # Выводим количество исходных и отфильтрованных рилсов
    print("----------------")
    print(f'count of input reels: {len(reelsData)}')
    print(f'count of filtered reels: {len(sorted_data)}')
    print("----------------")

    #Просто выписываем какие рилсы мы взяли и с каким количеством просмотров
    # for item in sorted_data:
    #     print(
    #         f'username: {item["ownerUsername"]}, shortcode: {item["shortCode"]}, views: {item["videoPlayCount"]}, timestamp: {item.get("timestamp", "N/A")}'  # Используем "N/A" если timestamp отсутствует
    #     )
    # print("----------------")
    sortedReelsCount = len(sorted_data)
    return reelsData, sorted_data, sortedReelsCount

def tiktok_scrapper_filter_sorter(dataset_items, request_dict, start_of_day, end_of_day):
    reelsData = []
    # Фильтруем только рилсы (type='Video'), которые попадают в целевые сутки (позавчера)
    for item in dataset_items:
        if 'uploadedAtFormatted' in item:
            # Парсим время публикации
            post_time = datetime.strptime(item['uploadedAtFormatted'], "%Y-%m-%dT%H:%M:%S.%fZ").date()  # Получаем только дату
            #print(post_time)
            # Проверяем, входит ли пост в диапазон целевых дат
            if start_of_day <= post_time <= end_of_day:
                reelsData.append(item)

    # Преобразуем request_dict в словарь для быстрого поиска, у меня тут появляется такой массив {'username_1': 2000, 'username_2':34000}
    username_limits = {
        entry['username']: entry['viewsFilter']
        for entry in request_dict
    }

    # Фильтруем рилсы
    filtered_reels = [
        reel for reel in reelsData
        if (reel['channel']['url'].split('@')[1].split('/')[0] in username_limits and 
            reel['views'] >= username_limits[reel['channel']['url'].split('@')[1].split('/')[0]])
    ]

    # Сортировка только по 'timestamp'
    sorted_data = sorted(
        filtered_reels,
        key=lambda x: (
            x.get('uploadedAtFormatted', 0)  # Используем 0 в качестве значения по умолчанию для timestamp, если он отсутствует
        )
    )

    # Выводим количество исходных и отфильтрованных рилсов
    print("----------------")
    print(f'count of input tiktok: {len(reelsData)}')
    print(f'count of filtered tiktok: {len(sorted_data)}')
    print("----------------")

    #Просто выписываем какие рилсы мы взяли и с каким количеством просмотров
    # for item in sorted_data:
    #     print(
    #         f'username: {item["authorMeta"]["name"]}, shortcode: {item["id"]}, views: {item["playCount"]}, timestamp: {item.get("createTimeISO", "N/A")}'  # Используем "N/A" если timestamp отсутствует
    #     )
    # print("----------------")
    sortedReelsCount = len(sorted_data)
    return reelsData, sorted_data, sortedReelsCount


def extracted_reels_data_maker(data):
    # Extracting the specified fields
    extracted_data = []
    for entry in data:
        try:
            # Initialize er_followers
            er_commlike = 0  # Initialize to avoid UnboundLocalError
            # Convert this format 2024-12-08T20:51:49.000Z to this 2024-12-06 00:57:56
            #print(f"time: {entry.get('timestamp')}")
            formatted_timestamp = datetime.strptime(
                str(entry.get('timestamp')),
                '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
            #print(f"time: {formatted_timestamp}")
            #convert this format 2024-12-08T20:51:49.000Z to this 2024-12-06 00:57:56
            
            #это нужно, чтобы убрать сокриэйтеров рилса
            username_real = entry.get('inputUrl').split('/')[-1]

            comments_count = float(entry.get('commentsCount', 0) or 0)
            likes_count = float(entry.get('likesCount', 0) or 0)
            video_play_count = float(entry.get('videoPlayCount', 1)
                                     or 1)  # Avoid division by zero
            if likes_count != -1:
                er_commlike = str(
                    round((comments_count + likes_count) / video_play_count,
                          10))
            else:
                er_commlike = 0

        except (ValueError, TypeError) as e:
            print(f"Error calculating engagement: {e}")
            er_commlike = 0

        extracted_entry = {
            'account_url': entry.get('inputUrl'),
            'username': username_real,
            'url': entry.get('url'),
            'timestamp': formatted_timestamp,
            'videoUrl': entry.get('videoUrl'),
            'shortCode': entry.get('shortCode'),
            'caption': entry.get('caption'),
            'commentsCount': entry.get('commentsCount'),
            'likesCount': entry.get('likesCount'),
            'collectCount': -1,
            'shareCount': entry.get('shareCount'),
            'videoPlayCount': entry.get('videoPlayCount'),
            'videoDuration': entry.get('videoDuration'),
            'er_commlike': er_commlike,
            'musicInfo': str(entry.get("musicInfo", {}).get("artist_name", "") + " - " + entry.get("musicInfo", {}).get("song_name", ""))
        }
        extracted_data.append(extracted_entry)

    return extracted_data


def extracted_tiktok_data_maker(data):
    # Extracting the specified fields
    extracted_data = []
    for entry in data:

        # Initialize er_followers
        er_all = 0
        er_shares = 0  # Initialize to avoid UnboundLocalError
        er_followers = 0  # Initialize to avoid UnboundLocalError
        try:


            # Convert ISO 8601 to a normal timestamp
            formatted_timestamp = datetime.strptime(
                str(entry.get('uploadedAtFormatted')),
                '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
            followers_count = float(entry.get("channel", {}).get("followers", 0))
            comments_count = float(entry.get('comments', 0))
            likes_count = float(entry.get('likes', 0))
            video_play_count = float(entry.get('views', 1))
            collect_count = float(entry.get('bookmarks', 0))
            share_count = float(entry.get('shares', 0))
            duration = entry.get("video", {}).get("duration", 0)
            
            if entry["video"]["duration"] is not None:
                duration = entry.get("video", {}).get("duration", 0)
            else:
                duration = "NoVideo"


            if likes_count != -1:
                er_all = str(
                    round((comments_count + likes_count + collect_count +
                           share_count) / video_play_count, 10))
            else:
                er_all = 0
            
            if entry.get('shares') != 0 and entry.get('views') != 0:
                er_shares = str( round( share_count / video_play_count, 10))
            else:
                er_shares = 0
            
            if entry["channel"]["followers"] != 0 and entry.get('views') != 0:
                er_followers = str( round( video_play_count / followers_count , 10))
            else:
                er_followers = 0


        except (ValueError, TypeError) as e:
            print(f"Error calculating engagement in id = {entry.get('id')}: {e}")

        extracted_entry = {
            'account_url': entry["channel"]["url"],
            'username': entry["channel"]["username"],
            'url': entry.get('postPage'),
            'timestamp': formatted_timestamp,
            'videoUrl': entry.get("video", {}).get("url", ""),
            'shortCode': entry.get('id'),
            'caption': entry.get('title'),
            'followersCount': entry.get("channel", {}).get("followers", 0),
            'commentsCount': entry.get('comments'),
            'likesCount': entry.get('likes'),
            'collectCount': entry.get('bookmarks'),
            'shareCount': entry.get('shares'),
            'videoPlayCount': entry.get('views'),
            'videoDuration': duration,
            'er_all': er_all,
            'er_shares': er_shares,
            'er_followers': er_followers,
            'musicInfo': str(entry.get("song", {}).get("artist", "") + " - " + entry.get("song", {}).get("title", ""))
        }
        extracted_data.append(extracted_entry)

    return extracted_data


#<FOR_TESTS1>
'''

'''
#</FOR_TESTS1>
#<FOR_TESTS2>
'''

'''
#</FOR_TESTS2>
