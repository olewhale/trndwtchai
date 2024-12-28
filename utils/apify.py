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


def instagram_posts_scrapper_4day(request_dict, days=2):
    # Инициализируем клиента Apify
    APIFY_API = os.getenv('APIFY_API')
    client = ApifyClient(APIFY_API)

    # Рассчитываем дату "позавчера"
    target_day = datetime.now() - timedelta(days=days)
    # Определяем начало и конец целевого дня
    start_of_day = target_day.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    daysOffsetFormate = start_of_day.strftime('%Y-%m-%d')

    # Извлекаем список username
    usernames = [
        item.get('username') for item in request_dict
        if isinstance(item, dict)
    ]
    
    run_input = {
        "username": usernames,
        "resultsLimit": 40,
        "onlyPostsNewerThan": daysOffsetFormate,
        "skipPinnedPosts":
        True  # Или True, если нужно пропускать закрепленные посты
    }
    print("Apify input created: " + str(run_input))
    
    reelsData = []
    # Запуск актора и ожидание его завершения
    try:
        run = client.actor("apify/instagram-post-scraper").call(
            run_input=run_input)
        dataset_items = client.dataset(
            run["defaultDatasetId"]).list_items().items
        
        print('--------')
        print('count of input items: ' + str(len(dataset_items)))
        print('-----')

        # Фильтруем только рилсы (type='Video'), которые попадают в целевые сутки (позавчера)
        for item in dataset_items:
            if 'type' in item and item['type'] == 'Video':
                # Парсим время публикации
                # Предполагаем формат времени: "2024-12-15T17:00:00.000Z"
                post_time = datetime.strptime(item['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")
                post_time = post_time.replace(tzinfo=pytz.utc)  # делаем aware

                # Проверяем, входит ли пост в диапазон позавчерашних суток
                if start_of_day <= post_time.replace(tzinfo=None) < end_of_day:
                    reelsData.append(item)

    except Exception as e:
        print(f"Error processing users: {e}")
    #print(reelsData)
    return reelsData


def instagram_posts_scrapper(request_dict, days=1):
    # Initialize the ApifyClient with your API token
    # Получаем ключ из переменных окружения
    APIFY_API = os.getenv('APIFY_API')

    # Инициализируем клиента
    client = ApifyClient(APIFY_API)

    # Получение X дней назад
    daysOffset = datetime.now() - timedelta(days=days)
    daysOffsetFormate = daysOffset.strftime('%Y-%m-%d')

    # Функция для получения постов списка из юзеров
    #users_list = request_dict.get("users", [])

    # Извлекаем все username и создаем run_input с объединением всех пользователей
    usernames = [
        item.get('username') for item in request_dict
        if isinstance(item, dict)
    ]

    run_input = {
        "username": usernames,
        "resultsLimit": 40,
        "onlyPostsNewerThan": daysOffsetFormate,
        "skipPinnedPosts":
        True  # Или True, если нужно пропускать закрепленные посты
    }
    print("Apify input created: " + str(run_input))
    
    reelsData = []
    # Запуск актора и ожидание его завершения
    try:
        #<last_version>
        run = client.actor("apify/instagram-post-scraper").call(
            run_input=run_input)
        dataset_items = client.dataset(
            run["defaultDatasetId"]).list_items().items
        #</last_version>
        #with open("db/13/potok_theexpertgarden_apify_20241227_174839.json", "r", encoding="utf-8") as file:
        #    dataset_items = json.load(file)
        # фильтрация только Reels('Video') из набора данных актора
        print('--------')
        print('count of input items: ' + str(len(dataset_items)))
        print('-----')
        for item in dataset_items:
            if 'type' in item and item['type'] == 'Video':
                reelsData.append(item)

    except Exception as e:
        print(f"Error processing users: {e}")
    #print(reelsData)
    return reelsData


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


def instagram_scrapper_filter_sorter(reelsData, request_dict):
    # Преобразуем request_dict в словарь для быстрого поиска, у меня тут появляется такой массив {'username_1': 2000, 'username_2':34000}
    username_limits = {
        entry['username']: entry['viewsFilter']
        for entry in request_dict
    }

    # Фильтруем рилсы
    filtered_reels = [
        reel for reel in reelsData
        if (reel['inputUrl'].split('/')[-1] in username_limits and 
            reel['videoPlayCount'] >= username_limits[reel['inputUrl'].split('/')[-1]])
    ]

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
    return sorted_data, sortedReelsCount


def extracted_reels_data_maker(data):
    # Extracting the specified fields
    extracted_data = []
    for entry in data:
        try:
            # Convert this format 2024-12-08T20:51:49.000Z to this 2024-12-06 00:57:56
            #print(f"time: {entry.get('timestamp')}")
            formatted_timestamp = datetime.strptime(
                str(entry.get('timestamp')),
                '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
            #print(f"time: {formatted_timestamp}")
            #convert this format 2024-12-08T20:51:49.000Z to this 2024-12-06 00:57:56
            comments_count = float(entry.get('commentsCount', 0) or 0)
            likes_count = float(entry.get('likesCount', 0) or 0)
            video_play_count = float(entry.get('videoPlayCount', 1)
                                     or 1)  # Avoid division by zero
            if likes_count != -1:
                engagement = str(
                    round((comments_count + likes_count) / video_play_count,
                          10))
            else:
                engagement = "-"

        except (ValueError, TypeError) as e:
            print(f"Error calculating engagement: {e}")
            engagement = 0

        extracted_entry = {
            'account_url': entry.get('inputUrl'),
            'username': entry.get('ownerUsername'),
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
            'engagement': engagement
        }
        extracted_data.append(extracted_entry)

    return extracted_data


def extracted_tiktok_data_maker(data):
    # Extracting the specified fields
    extracted_data = []
    for entry in data:
        try:
            # Convert ISO 8601 to a normal timestamp
            formatted_timestamp = datetime.strptime(
                str(entry.get('createTimeISO')),
                '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
            comments_count = float(entry.get('commentCount', 0))
            likes_count = float(entry.get('diggCount', 0))
            video_play_count = float(entry.get('playCount', 1))
            collect_count = float(entry.get('collectCount', 0))
            share_count = float(entry.get('shareCount', 0))

            if likes_count != -1:
                engagement = str(
                    round((comments_count + likes_count + collect_count +
                           share_count) / video_play_count, 10))
            else:
                engagement = "-"

        except (ValueError, TypeError) as e:
            print(f"Error calculating engagement: {e}")
            engagement = 0

        extracted_entry = {
            'account_url': entry["authorMeta"]["profileUrl"],
            'username': entry["authorMeta"]["name"],
            'url': entry.get('webVideoUrl'),
            'timestamp': formatted_timestamp,
            'videoUrl':
            entry.get('mediaUrls')[0] if entry.get('mediaUrls') else None,
            'shortCode': entry.get('id'),
            'caption': entry.get('text'),
            'commentsCount': entry.get('commentCount'),
            'likesCount': entry.get('diggCount'),
            'collectCount': entry.get('collectCount'),
            'shareCount': entry.get('shareCount'),
            'videoPlayCount': entry.get('playCount'),
            'videoDuration': entry.get('videoDuration'),
            'engagement': engagement
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
