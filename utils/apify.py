import os, sys, json
from apify_client import ApifyClient
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pytz
import math
from concurrent.futures import ThreadPoolExecutor, as_completed


# Загружаем переменные из .env
load_dotenv()

# Convert ISO 8601 to a normal timestamp
#formatted_timestamp = datetime.strptime('2024-10-03T00:22:51.000Z', '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')

# doesn't work yet. it should
def instagram_user_scrapper(request_dict):
    #Script that get count of followers use this apify actor - its free! =)
    #https://console.apify.com/actors/xMBzmb4DgNHnkOn4q/input
    return None


def instagram_posts_scrapper_old_10_02_2025(request_dict, start_of_day, days=3, range_days=None):
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

def instagram_posts_scrapper(request_dict, start_of_day, days=3, range_days=None):
    # Загружаем переменные из .env
    #load_dotenv()
    
    # Инициализируем клиента Apify (синхронно)
    APIFY_API = "apify_api_yWpkjSErkoE8elqnfrRcQAjwNmJPc92UqMym"
    client = ApifyClient(APIFY_API)

    # # Получаем информацию об аккаунте Apify
    # try:
    #     account_info = client.user().get()
    #     print("Apify account username:", account_info.get("username"))
    # except Exception as e:
    #     print("Ошибка при получении информации об аккаунте:", e)
    
    # Рассчитываем даты для фильтрации
    if range_days:
        start_range, end_range = map(int, range_days.split('-'))
        computed_start_of_day = (datetime.now() - timedelta(days=end_range)).date()
        computed_end_of_day = (datetime.now() - timedelta(days=start_range)).date()
    else:
        target_day = datetime.now() - timedelta(days=days)
        computed_start_of_day = target_day.date()
        computed_end_of_day = (target_day + timedelta(days=1)).date()
    
    print("Computed start_of_day:", computed_start_of_day)
    print("Computed end_of_day:", computed_end_of_day)
    
    # Извлекаем список username из request_dict
    usernames = [item.get('username') for item in request_dict 
                 if isinstance(item, dict) and item.get('username')]
    if not usernames:
        print("No usernames found in request_dict!")
        return []
    print("Usernames extracted:", usernames)
    
    # Преобразуем username в полные ссылки для Instagram
    username_links = [f"https://www.instagram.com/{user}" for user in usernames]
    print("Username links:", username_links)
    
    # Функция для разбиения списка на чанки заданного размера
    def chunk_list(lst, chunk_size):
        for i in range(0, len(lst), chunk_size):
            yield lst[i:i + chunk_size]
    
    chunk_size = 20  # Можно менять размер чанка, если нужно
    username_chunks = list(chunk_list(username_links, chunk_size))
    print("Total chunks formed:", len(username_chunks))
    
    # Синхронная функция для вызова актора Apify для одного чанка
    def run_actor_sync(chunk):
        run_input = {
            "customMapFunction": "(object) => { return {...object} }",
            "maxItems": 1500,
            "startUrls": chunk,
            "until": computed_start_of_day.strftime('%Y-%m-%d')
        }
        print("Sending request with input:", run_input)
        try:
            run = client.actor("apidojo/instagram-scraper").call(run_input=run_input)
            #print("Received run response:", run)
            dataset_items = client.dataset(run["defaultDatasetId"]).list_items().items
            print("Dataset items count:", len(dataset_items))
            return dataset_items
        except Exception as e:
            print(f"[run_actor_sync] Error processing chunk {chunk}: {e}")
            return []
    
    combined_results = []
    # Запускаем задачи параллельно через ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_index = { executor.submit(run_actor_sync, chunk): idx 
                            for idx, chunk in enumerate(username_chunks) }
        for future in as_completed(future_to_index):
            idx = future_to_index[future]
            try:
                result = future.result()
                combined_results.extend(result)
                print(f"Chunk {idx + 1}: {len(result)} items received.")
            except Exception as e:
                print(f"[main] Error processing chunk {idx + 1}: {e}")
    
    print("--------")
    print("Total count of input items:", len(combined_results))
    print("-----")
    
    return combined_results

def tiktok_posts_scrapper_old_10_02_2025(request_dict, search_type, start_of_day, days=3, range_days=None):
    # Загружаем переменные из .env
    load_dotenv()
    # Инициализируем клиента Apify
    APIFY_API = os.getenv('APIFY_API')
    #client = ApifyClient(APIFY_API)
    client = ApifyClient("apify_api_Mh8rUvYzbCNWJJbHyh8okswsRTA39z1cA3BD")

    if search_type == "username":
        # Извлекаем список username
        usernames = [
            item.get('username') for item in request_dict
            if isinstance(item, dict)
        ]
        
        run_input = {
            "maxItems": 5000,
            "until": start_of_day.strftime('%Y-%m-%d'),
            "usernames": usernames
        }

    elif search_type == "hashtag":
        # Извлекаем список username
        hashtags = [
            item.get('hashtag') for item in request_dict #здесь берутся хэштеги. Надо будет поправить это.
            if isinstance(item, dict)
        ]
        
        run_input = {
            "maxItems": 5000,
            "dateRange": "THIS_WEEK",
            "keywords": hashtags
        } 


    print("Apify input created: " + str(run_input))
    
    #print("Локальные переменные:", json.dumps(locals(), default=str, ensure_ascii=False, indent=4))
    #sys.exit()

    
    # Запуск актора и ожидание его завершения
    try:
        if search_type == "username":
            run = client.actor("apidojo/tiktok-profile-scraper").call(
                run_input=run_input)
            dataset_items = client.dataset(
                run["defaultDatasetId"]).list_items().items
        elif search_type == "hashtag":
            run = client.actor("apidojo/tiktok-scraper").call(
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



def tiktok_posts_scrapper(request_dict, search_type, start_of_day, days=3, range_days=None):
    # Загружаем переменные из .env
    load_dotenv()
    
    # Инициализируем клиента Apify (синхронно)
    APIFY_API = "apify_api_yWpkjSErkoE8elqnfrRcQAjwNmJPc92UqMym"
    client = ApifyClient(APIFY_API)
    
    # Здесь можно добавить логику для перерасчёта дат, если потребуется.
    
    # Функция для разбиения списка на чанки заданного размера
    def chunk_list(lst, chunk_size):
        for i in range(0, len(lst), chunk_size):
            yield lst[i:i + chunk_size]
    
    combined_results = []
    # Разбиваем список на чанки (например, по 5 hashtag)
    chunk_size = 15
    
    if search_type == "username":
        # Извлекаем список username
        usernames = [item.get('username') for item in request_dict 
                     if isinstance(item, dict) and item.get('username')]
        
        username_chunks = list(chunk_list(usernames, chunk_size))
        
        # Функция-воркер для обработки одного чанка username
        def run_actor_sync(chunk):
            run_input = {
                "maxItems": 1500,
                "until": start_of_day.strftime('%Y-%m-%d'),
                "usernames": chunk
            }
            try:
                print("Running TikTok username actor with input:", run_input)
                run = client.actor("apidojo/tiktok-profile-scraper").call(run_input=run_input)
                dataset_items = client.dataset(run["defaultDatasetId"]).list_items().items
                return dataset_items
            except Exception as e:
                print(f"[run_actor_sync] Ошибка при обработке чанка {chunk}: {e}")
                return []
        
        # Параллельный запуск воркеров через ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_index = {executor.submit(run_actor_sync, chunk): idx 
                               for idx, chunk in enumerate(username_chunks)}
            
            for future in as_completed(future_to_index):
                idx = future_to_index[future]
                try:
                    result = future.result()
                    combined_results.extend(result)
                    print(f"Chunk {idx + 1}: {len(result)} items received.")
                except Exception as e:
                    print(f"[main] Ошибка в обработке чанка {idx + 1}: {e}")
    
    elif search_type == "hashtag":
        # Извлекаем список hashtag
        hashtags = [item.get('hashtag') for item in request_dict 
                    if isinstance(item, dict) and item.get('hashtag')]
        
        hashtag_chunks = list(chunk_list(hashtags, chunk_size))
        
        # Функция-воркер для обработки одного чанка hashtag
        def run_actor_sync(chunk):
            run_input = {
                "maxItems": 1500,
                "dateRange": "THIS_WEEK",
                "keywords": chunk
            }
            try:
                print("Running TikTok hashtag actor with input:", run_input)
                run = client.actor("apidojo/tiktok-scraper").call(run_input=run_input)
                dataset_items = client.dataset(run["defaultDatasetId"]).list_items().items
                return dataset_items
            except Exception as e:
                print(f"[run_actor_sync] Ошибка при обработке чанка {chunk}: {e}")
                return []
        
        # Параллельный запуск воркеров через ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_index = {executor.submit(run_actor_sync, chunk): idx 
                               for idx, chunk in enumerate(hashtag_chunks)}
            
            for future in as_completed(future_to_index):
                idx = future_to_index[future]
                try:
                    result = future.result()
                    combined_results.extend(result)
                    print(f"Chunk {idx + 1}: {len(result)} items received.")
                except Exception as e:
                    print(f"[main] Ошибка в обработке чанка {idx + 1}: {e}")
    else:
        print(f"Unsupported search_type: {search_type}")
        return []
    
    print('--------')
    print('Total count of input items: ' + str(len(combined_results)))
    print('-----')
    
    return combined_results




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
    
    # Удаляем дублирующие элементы по ['code']
    print(f'Before duplicates {len(reelsData)}')
    unique_reels = {}
    for reel in reelsData:
        unique_reels[reel['code']] = reel
    reelsData = list(unique_reels.values())

    print(f'After duplicates {len(reelsData)}')
    
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
        elif username not in username_limits and play_count >= 100000:
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

def tiktok_scrapper_filter_sorter(dataset_items, request_dict, search_type, start_of_day, end_of_day):
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

    # Удаляем дублирующие элементы по ['code']
    print(f'Before duplicates {len(reelsData)}')
    unique_reels = {}
    for reel in reelsData:
        unique_reels[reel['id']] = reel
    reelsData = list(unique_reels.values())

    print(f'After duplicates {len(reelsData)}')


    if search_type == "username":
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
    elif search_type == "hashtag":
        # Преобразуем request_dict в словарь для быстрого поиска, у меня тут появляется такой массив {'username_1': 2000, 'username_2':34000}
        username_limits = {
            entry['hashtag']: entry['likesFilter']
            for entry in request_dict
        }   

        print(f"Filter for hashtags = {request_dict[0]['likesFilter']}")
        filtered_reels = [
            reel for reel in reelsData
            if reel.get('likes', 0) >= request_dict[0]['likesFilter']
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
            er_followers = 0
            musicInfo = ""
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
            followers_count = float(entry.get('owner', {}).get('followerCount','') or 1)


            if likes_count != -1:
                er_commlike = float(
                    round((comments_count + likes_count) / video_play_count,
                          10))
            else:
                er_commlike = 0


            if entry.get("audio") is not None:
                musicInfo = str(entry.get("audio", {}).get("artist", "") + " - " + entry.get("audio", {}).get("title", ""))
            else:
                musicInfo = ""

            
            if followers_count > 0 and video_play_count > 0:
                er_followers = float(round(video_play_count / followers_count, 10)) 
            else:
                er_followers = 0
            # print(f"shortcode - {entry.get('code')}")
            # print(f"{comments_count}   -   {likes_count}   -   {video_play_count}   -   {followers_count}")
            # print(f"{er_commlike}   -   {er_followers}   -   {musicInfo}")           
                

        except (ValueError, TypeError) as e:
            print(f"Error calculating engagement: {e}")
            er_commlike = 0




        extracted_entry = {
            'account_url': username_link,
            'username': username_real,
            'url': entry.get('url'),
            'platform': "instagram",
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Добавляем дату и время создания элемента
            'timestamp': formatted_timestamp,
            'videoUrl': entry.get('video', {}).get('url',''),
            'shortCode': entry.get('code'),
            'caption': entry.get('caption'),
            'followersCount': followers_count,
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
        musicInfo = ""
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
                er_followers = float(round(video_play_count / followers_count, 10)) 
            else:
                er_followers = 0

            if entry["song"]["artist"] is not None:
                if entry["song"]["title"] and "original sound" not in entry["song"]["title"]:
                    musicInfo = str(entry.get("song", {}).get("artist", "") + " - " + entry.get("song", {}).get("title", ""))
                else:
                    musicInfo = ""
            else:
                musicInfo = ""
            

        except (ValueError, TypeError) as e:
            print(f"Error calculating engagement in id = {entry.get('id')}: {e}")

        extracted_entry = {
            'account_url': entry["channel"]["url"],
            'username': entry["channel"]["username"],
            'url': entry.get('postPage'),
            'platform': "tiktok",
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Добавляем дату и время создания элемента
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
            'musicInfo': musicInfo
        }
        extracted_data.append(extracted_entry)

    return extracted_data
