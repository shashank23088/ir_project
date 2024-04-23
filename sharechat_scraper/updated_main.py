#!/usr/bin/env python
# coding: utf-8

import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import chromedriver_autoinstaller
import json
from constants import tag_urls, perTagLimit, outputName, lang
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
import requests
from urllib.parse import urlparse, unquote
import urllib

# print("Installing chromedriver!")
# chromedriver_autoinstaller.install()
# print("Done.")

main_data_folder = 'updated_data'
if not os.path.exists(main_data_folder):
    os.makedirs(main_data_folder)

# Function to download and save media
import base64
import re

import os
import requests
import base64
import re
from PIL import Image
from io import BytesIO

main_data_folder = "updated_data"  # Folder to store downloaded media

valid_image_extensions = "jpg,png,jpeg".split(',')

def download_media(url, media_type, post_ph, user_id, folder_path):
    print(f"\nGetting image: {url}\n")
    try:
        # Check if the URL is a base64-encoded data URI
        if url.startswith('data:image'):

            print("Skipping Base64 Encoded Image!")
            return None

            # Decode the base64-encoded image and save it
            data = re.search(r'base64,(.*)', url).group(1)
            image_data = base64.b64decode(data)
            
            # Save the file in the data folder with the post_ph as the filename
            folder_name = str(user_id)  # Convert user_id to string
            filename = f'{folder_path}/{post_ph}.jpeg'
            
            with open(filename, 'wb') as file:
                file.write(image_data)
            
            print(f"Downloaded base64-encoded image: {filename}")
            return filename
        else:
            # Get the file extension from the URL
            _, file_extension = os.path.splitext(url)
            file_extension = file_extension.lower()  # Ensure lowercase for consistency

            # Skip any svg files
            if file_extension == '.svg':
                print(f"Skipping SVG File!")
                return None

            response = requests.get(url, stream=True)
            if response.status_code == 200:
                # Save the file in the data folder with the post_ph as the filename
                folder_name = str(user_id)  # Convert user_id to string
                filename = f'{folder_path}/{post_ph}{file_extension}'
                with open(filename, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=128):
                        file.write(chunk)
                print(f"Downloaded {media_type}: {filename}")
                return filename
            else:
                print("Could not fetch image!")
                return None
    except Exception as e:
        print("An error occurred while downloading media:", str(e))
        return None


# Rest of the code remains unchanged

def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text)




# Set the display environment variable
os.environ['DISPLAY'] = ':1'

# URL of the ShareChat page
url = f"https://sharechat.com/trending/{lang}"


# chromedriver_autoinstaller.install()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-popup-blocking')
# Overcomes limited resource problems
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")  # Applicable to windows os only
chrome_options.add_argument(
    "--remote-debugging-port=9222")  # This is important
# Disable sandboxing that Chrome runs in.
chrome_options.add_argument("--no-sandbox")


from selenium.webdriver.chrome.service import Service
# service = Service(executable_path='./chromedriver120')
service = Service(executable_path='/usr/lib/chromium-browser/chromedriver')

driver = webdriver.Chrome(service=service, options=chrome_options)

# tag_url = "https://sharechat.com/tag/G7qd0K"

print(url)

driver.get(url)
time.sleep(2)
post_done = set()
if os.path.exists(outputName):
    # read
    with open(outputName, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            post_done.add(data['post_ph'])

outputJsonL = open(outputName, 'a', encoding='utf-8')

keepRunning = True
for tag_url in tag_urls:

    data_folder_tag = f'updated_data/{tag_url.split("/")[-1]}_{lang}'
    
    if not os.path.exists(data_folder_tag):
        os.makedirs(data_folder_tag)

    if not keepRunning:
        break
    postsDone = 0
    driver.get(tag_url)
    print(tag_url)
    while keepRunning:
        time.sleep(2)

        scroller = driver.find_element(By.XPATH,
                                       "//div[@class='infinite-list-wrapper']")
        newPosts = False
        posts = scroller.find_elements(
            By.XPATH, './/div[@data-cy="link-post"] | .//div[@data-cy="image-post"] | //div[@data-cy="video-post"] | //div[@data-cy="gif-post"]')

        for post in posts:
            try:
                # get the data-post-ph attribute of post
                post_ph = post.get_attribute('data-post-ph')
                if post_ph in post_done:
                    print("Post already done:", post_ph)
                    continue

                newPosts = True

                print("Post PH:", post_ph)

                post_done.add(post_ph)
                # Locate the elements containing the information
                author_element = post.find_element(
                    By.CSS_SELECTOR, 'strong[data-cy="author-name"]')
                author_name = author_element.text

                author_link_element = post.find_element(
                    By.CSS_SELECTOR, 'a[data-cy="avatar-tag"]')

                author_link = author_link_element.get_attribute('href')

                authorID = author_link[author_link.find('/profile/') +
                                       len('/profile/'):author_link.find('?referer=')]

                topDetailsDiv = post.find_element(
                    By.XPATH, './/div[@class="H(100%) Pstart($xs) Fxg(1) Miw(0)"]')

                # find direct div inside it
                topDetailsDiv = topDetailsDiv.find_element(
                    By.XPATH, './div[@class="H(100%) Ta(start) D(f) Jc(c) Ai(fs) Fxd(c)"]')

                # direct divs inside it
                innerDivs = topDetailsDiv.find_elements(
                    By.XPATH, './div')
                text = innerDivs[1].text.split('•')
                years_before = text[1].strip()
                number_of_views = text[0].strip()

                # post_caption = post.find_element(
                #     By.XPATH, './/div[@data-cy="post-caption"]')
                # pcText = post_caption.text

                # print(f"Post by {author_name} [{authorID}]")
                # print("Author Name:", author_name)
                # print("Caption:", pcText)
                # print("Author Link:", author_link)
                # print("Author ID:", authorID)
                # print("Number of Views:", number_of_views)
                # print("Years Before:", years_before)
                # print("Post Caption:", pcText)

                # open new page comments
                commentLink = f"https://sharechat.com/comment/{post_ph}"
                print("Number of windows:", len(driver.window_handles))

                original_window = driver.current_window_handle

                driver.execute_script(f"window.open('{commentLink}');")
                time.sleep(1)
                # reload

                new_window = [
                    window for window in driver.window_handles if window != original_window][0]
                driver.switch_to.window(new_window)
                # toFindinLike = "लाइक"
                # toFindinComment = "कमेंट"
                toFindinLike = "পছন্দ"
                toFindinComment = "মন্তব্য"

                maxTriesFind = 5
                tries = 0
                while toFindinLike not in driver.page_source:
                    driver.refresh()
                    time.sleep(1)
                    tries += 1

                    if tries > maxTriesFind:
                        break

                if tries > maxTriesFind:
                    driver.close()
                    driver.switch_to.window(original_window)
                    continue

                time.sleep(1)

                topBar = driver.find_element(
                    By.XPATH, '//ul[@class="List(n)  D(f) Ai(c) W(100%) H(100%) "]')

                idx = 0

                topEls = topBar.find_elements(By.XPATH, './li')
                for idx, li in enumerate(topEls):
                    if toFindinLike in li.text:
                        break

                likeCount = int(topEls[idx].text.replace(
                    toFindinLike, '').strip())
                print("Likes: ", likeCount)

                idx2 = 0
                for idx2, li in enumerate(topEls):
                    if toFindinComment in li.text:
                        break

                commentCount = int(topEls[idx2].text.replace(
                    toFindinComment, '').strip())
                print("Comments: ", commentCount)

                # COMMENTS SCRAPING
                mainDiv = driver.find_element(
                    By.XPATH, '//div[@class="Ovy(a) Fxg(1) W(100%) Maw(600px) M(a)"]')

                # loadedComments = len(mainDiv.find_elements(
                #     By.XPATH, './/div[@class="Px($sm) Pt($xs) Mb($xs) Bgc($white)"]'))

                # pbar = tqdm(total=commentCount)
                # scroll_increment = 100  # The amount by which to increment the scroll each time
                # current_scroll_position = 0  # Keep track of the current scroll position

                # checkFinishTimer = 5
                # startTimer = time.time()
                # sameSize = False
                # retried = False
                # while not sameSize or not retried:
                #     time.sleep(0.1)
                #     driver.execute_script(
                #         f"arguments[0].scrollTop = {current_scroll_position}", mainDiv)

                #     if sameSize:
                #         # scroll up a bit
                #         retried = True
                #         sameSize = False
                #         driver.execute_script(
                #             f"arguments[0].scrollTop = {current_scroll_position - 50}", mainDiv)

                #         continue
                #     current_scroll_position += scroll_increment

                #     if time.time() - startTimer > checkFinishTimer:
                #         listEls = mainDiv.find_elements(
                #             By.XPATH, './/div[@class="Px($sm) Pt($xs) Mb($xs) Bgc($white)"]')
                #         if len(listEls) == loadedComments:
                #             sameSize = True
                #             if retried:
                #                 break

                #         else:
                #             retried = False
                #             sameSize = False
                #         loadedComments = len(listEls)

                #         pbar.update(loadedComments - pbar.n)
                #         startTimer = time.time()

                # pbar.close()
                # time.sleep(2)

                # # get the list of all the comments
                # listEls = mainDiv.find_elements(
                #     By.XPATH, './/div[@class="Px($sm) Pt($xs) Mb($xs) Bgc($white)"]')

                # comments = {}
                # users = []
                # for li in listEls:
                #     nameA = li.find_elements(
                #         By.XPATH, './/a[@class="Lh(20px) Mb($xs) Pend($xs) Whs(nw) Ovx(h) Tov(e) Maw(100%) C($bcBlue)"]')

                #     if len(nameA) == 0:
                #         continue

                #     if len(nameA) > 1:
                #         print("More than 1 nameA in comments")
                #         continue

                #     # get href
                #     href = nameA[0].get_attribute('href')
                #     # start after /profile/ from beginning, no need to find ?referrer=url from end
                #     profile = href[href.find('/profile/') +
                #                    len('/profile/'):]

                #     users.append(profile)

                #     if profile not in comments:
                #         comments[profile] = []

                #     contentDiv = li.find_elements(
                #         By.XPATH, './/div[@class="Pend($2xl)"]')
                #     if len(contentDiv) == 0:
                #         continue

                #     commentStructure = {"text": "",
                #                         "images": [], "sentiment": "N/A"}
                #     for div in contentDiv:
                #         # get text from div
                #         text = div.text
                #         # add all img sources
                #         imgs = div.find_elements(By.XPATH, './/img')
                #         for img in imgs:
                #             commentStructure["images"].append(
                #                 img.get_attribute('src'))
                #         commentStructure["text"] += text
                #         if len(commentStructure["text"]) > 0:
                #             commentStructure["sentiment"] = analyze_sentiment(
                #                 commentStructure["text"])

                #     comments[profile].append(commentStructure)

                # print("Comments:", comments)

                # LIKES SCRAPING
                # click
                topEls[idx].click()

                mainDiv = driver.find_element(
                    By.XPATH, '//div[@class="Ovy(a) Fxg(1) W(100%) Maw(600px) M(a)"]')

                # loadedlikes = number of a
                loaded_likes = len(mainDiv.find_elements(
                    By.XPATH, './/a[@data-cy="avatar-tag"]'))
                pbar = tqdm(total=likeCount)
                scroll_increment = 100  # The amount by which to increment the scroll each time
                current_scroll_position = 0  # Keep track of the current scroll position

                checkFinishTimer = 5
                startTimer = time.time()
                sameSize = False
                retried = False
                while not sameSize or not retried:
                    time.sleep(0.1)
                    driver.execute_script(
                        f"arguments[0].scrollTop = {current_scroll_position}", mainDiv)

                    if sameSize:
                        # scroll up a bit
                        retried = True
                        sameSize = False
                        driver.execute_script(
                            f"arguments[0].scrollTop = {current_scroll_position - 50}", mainDiv)

                        continue
                    current_scroll_position += scroll_increment

                    if time.time() - startTimer > checkFinishTimer:
                        listEls = mainDiv.find_elements(
                            By.XPATH, './/a[@data-cy="avatar-tag"]')
                        if len(listEls) == loaded_likes:
                            sameSize = True
                            if retried:
                                break

                        else:
                            retried = False
                            sameSize = False
                        loaded_likes = len(listEls)

                        pbar.update(loaded_likes - pbar.n)
                        startTimer = time.time()

                pbar.close()
                time.sleep(1)

                # get the list of all the users
                # listEls = mainDiv.find_elements(
                #     By.XPATH, './/a[@data-cy="avatar-tag"]')

                # in this, strong tag with data-cy="author-name" is the name of the user, get it
                # and add it to a list

                # justLikes = []
                # for li in listEls:
                #     # get href value
                #     href = li.get_attribute('href')
                #     # start after /profile/ from beginning and ?referrer=url from end
                #     profile = href[href.find('/profile/') +
                #                    len('/profile/'):href.find('?referer=')]
                #     users.append(profile)
                #     justLikes.append(profile)

                # if authorID not in users:
                #     users.append(authorID)

                # users = list(set(users))

                # print("Users:", users)
                # print("Number of users:", len(users))
                driver.close()
                driver.switch_to.window(original_window)

                # followers = {}

                # to-remove: comments, justLikes, pcText, author_name

                curData = {
                    "post_ph": post_ph,
                    # "author_name": author_name,
                    "author_url": author_link,
                    "author_id": authorID,
                    "number_of_views": number_of_views,
                    "years_before": years_before,
                    # "post_caption": pcText,
                    "likes": likeCount,
                    # "comments": comments,
                    # "like_users": justLikes,
                    # "all_users": users,
                    # "followers": followers,
                    "tag": tag_url
                }
                print("Data:", curData)

                outputJsonL.write(json.dumps(curData, ensure_ascii=False) + '\n')
                outputJsonL.flush()
                postsDone += 1

                # user_folder = f'{data_folder}/{author_name}'
                # if not os.path.exists(user_folder):
                #     os.makedirs(user_folder)

                # Downloading photos/ videos
                image_elements = post.find_elements(By.XPATH, './/img')
                for idx, img in enumerate(image_elements):
                    img_src = img.get_attribute("data-src")
                    if img_src is None:
                        img_src = img.get_attribute('src')
                    # or ("data:image" in img_src.lower()) # Additional Condition
                    if (img_src.lower().split('.')[-1] in valid_image_extensions):
                        img_filename = download_media(img_src, f'image_{idx}', post_ph, author_name, data_folder_tag)
                        if img_filename:
                            print(f"Downloaded image: {img_filename}")

                # media_elements = post.find_elements(By.XPATH, './/img | .//video')
                media_elements = post.find_elements(By.XPATH, './/video')
                for idx, media in enumerate(media_elements):
                    media_src = media.get_attribute("data-src")
                    if media_src is None:
                        media_src = media.get_attribute("src")
                    # media_type = 'image' if (media_src.lower().split('.')[-1] in valid_image_extensions) else 'video'
                    media_type = 'video'
                    media_filename = download_media(media_src, f'{media_type}_{idx}', post_ph, author_name, data_folder_tag)
                    if media_filename:
                        print(f"Downloaded {media_type}: {media_filename}")

            except KeyboardInterrupt:
                keepRunning = False
                print("Keyboard Interrupt... Exiting")
                break
            except Exception as e:
                print("An error occurred:", str(e))
                continue

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(5)
        if not newPosts or postsDone >= perTagLimit:
            break

        if not keepRunning:
            break

    outputJsonL.close()

    driver.quit()