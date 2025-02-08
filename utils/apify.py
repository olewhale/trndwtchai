import os, sys, json
from apify_client import ApifyClient
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pytz
import math

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
    client = ApifyClient("apify_api_yWpkjSErkoE8elqnfrRcQAjwNmJPc92UqMym")


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
    # apify actor
    # run_input = {
    #     "username": usernames,
    #     "resultsLimit": 70,
    #     "onlyPostsNewerThan": start_of_day.strftime('%Y-%m-%d'),
    #     "skipPinnedPosts":
    #     True  # Или True, если нужно пропускать закрепленные посты
    # }

        ###
    #apidojo/instagram-scraper
    ###

    # Prepend "https://www.instagram.com/" to each link
    username_links = [f"https://www.instagram.com/{user}" for user in usernames]   

    run_input = {
        "customMapFunction": "(object) => { return {...object} }",
        "maxItems": 5000,
        "startUrls": username_links,
        "until": start_of_day.strftime('%Y-%m-%d')
    }

    ###
    #END____apidojo/instagram-scraper
    ###

    print("Apify input created: " + str(run_input))
    
    #print("Локальные переменные:", json.dumps(locals(), default=str, ensure_ascii=False, indent=4))
    #sys.exit()

    # Запуск актора и ожидание его завершения
    try:
        run = client.actor("apidojo/instagram-scraper").call(
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
    
    ###
    #END____apify_instagram-scraper
    ###


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
        if 'isVideo' in item and item['isVideo'] == True:
            # Парсим время публикации
            post_time = datetime.strptime(item['createdAt'], "%Y-%m-%dT%H:%M:%S.%fZ").date()  # Получаем только дату
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
    filtered_reels = []
    for reel in reelsData:
        username = reel.get('owner', {}).get('username', '')  # Исправлено 'onwer' -> 'owner'
        play_count = reel.get('video', {}).get('playCount', 0) #ВОЗМОЖНО ЭТО ПЛОХО ОТРАБАТЫВАЕТ И ВЫСТАВЛЯЕТ 0

        # Skip this reel if it contains 'noResults'
        if 'noResults' in reel:
            continue  

        if username in username_limits and play_count >= username_limits[username]:
            filtered_reels.append(reel)
        #elif play_count >= 20000:
        elif username not in username_limits and play_count >= 20000:
            print(f"\033[94mReels from user that not in database - {reel.get('owner', {}).get('username', 'NOOOOOOO')} - views:  {reel.get('video', {}).get('playCount', 0)}\033[0m")
            # Если username отсутствует в username_limits, добавляем его и включаем рилс в список
            username_limits.setdefault(username, 0)
            filtered_reels.append(reel)





    # CUSTOM FILTER - НЕ БУДЕТ РАБОТАТЬ, ТАК КАК ЗАМЕНЕН ACTOR APIFY!!!
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
            x.get('createdAt', 0)  # Используем 0 в качестве значения по умолчанию для timestamp, если он отсутствует
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

    # Фильтруем видео
    filtered_reels = [
        reel for reel in reelsData
        if (reel['channel']['url'].split('@')[1].split('/')[0] in username_limits and 
            reel['views'] >= username_limits[reel['channel']['url'].split('@')[1].split('/')[0]])
    ]

    # Фильтруем видео
    # filtered_reels = [
    #     reel for reel in reelsData
    #     if reel.get('likes', 0) >= 10000
    # ]

    # for reel in filtered_reels:
    #     print(f"{reel['channel']['username']} - {reel.get('likes', 0)}")

    # sys.exit()

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
                str(entry.get('createdAt')),
                '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
            #print(f"time: {formatted_timestamp}")
            #convert this format 2024-12-08T20:51:49.000Z to this 2024-12-06 00:57:56
            
            #это нужно, чтобы убрать сокриэйтеров рилса - ПОСЛЕ ДОБАВЛЕНИЯ нового эктора убрал эту функцию
            #username_real = entry.get('inputUrl').split('/')[-1]
            username_real = entry.get('owner', {}).get('username','')
            # Prepend "https://www.instagram.com/" to each link
            username_link = f"https://www.instagram.com/{username_real}"   

            comments_count = float(entry.get('commentCount', 0) or 0)
            likes_count = float(entry.get('likeCount', 0) or 0)
            video_play_count = float(entry.get('video', {}).get('playCount','') or 1)  # Avoid division by zero
            followers_сount = float(entry.get('owner', {}).get('followerCount','') or 1)

            if likes_count != -1:
                er_commlike = str(
                    round((comments_count + likes_count) / video_play_count,
                          10))
            else:
                er_commlike = 0

            if entry.get("audio") is not None:
                musicInfo = str(entry.get("audio", {}).get("artist", "") + " - " + entry.get("audio", {}).get("title", ""))
            else:
                musicInfo = ""
            
            if likes_count != -1:
                er_commlike = str(
                    round((comments_count + likes_count) / video_play_count,
                          10))
            else:
                er_commlike = 0
            
            # if entry.get('shares') != 0 and entry.get('views') != 0:
            #     er_shares = str( round( share_count / video_play_count, 10))
            # else:
            #     er_shares = 0
            
            if followers_сount > 0 and entry.get('views', 0) > 0:
                er_followers = str(round(math.log(1 + video_play_count) / math.log(1 + followers_сount), 10))
            else:
                er_followers = 0
            
                

        except (ValueError, TypeError) as e:
            print(f"Error calculating engagement: {e}")
            er_commlike = 0




        extracted_entry = {
            'account_url': username_link,
            'username': username_real,
            'url': entry.get('url'),
            'timestamp': formatted_timestamp,
            'videoUrl': entry.get('video', {}).get('url',''),
            'shortCode': entry.get('code'),
            'caption': entry.get('caption'),
            'followersCount': followers_сount,
            'commentsCount': comments_count,
            'likesCount': likes_count,
            'collectCount': 0,
            'shareCount': 0,
            'videoPlayCount': video_play_count,
            'videoDuration': entry.get('video', {}).get('duration', 0),
            'er_commlike': er_commlike,
            'er_shares': 0,
            'er_followers': er_followers,
            'musicInfo': musicInfo
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
            followers_count = entry.get("channel", {}).get("followers", 0)
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
            
            if entry.get('shares') > 0 and entry.get('views') > 0:
                er_shares = str( round( share_count / video_play_count, 10))
            else:
                er_shares = 0
            
            if followers_count > 0 and entry.get('views', 0) > 0:
                er_followers = str(round(math.log(1 + video_play_count) / math.log(1 + followers_count), 10))
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
