def scrape(x):

    import sys
    import os
    import bs4
    import requests
    import pprint
    import pandas as pd
    from splinter import Browser
    import splinter
    browser = Browser('firefox', headless=True)

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = bs4.BeautifulSoup(response.text, 'lxml')

    ### Show RAW format
    pprint.pprint(soup)

    body_data = soup.body

    # Print all ten headlines
    tds = body_data.find_all('td')
    # A blank list to hold the headlines
    headlines = []
    # Loop over td elements
    for td in tds:
        # If td element has an anchor...
        if (td.a):
            # And the anchor has non-blank text...
            if (td.a.text):
                # Append the td to the list
                headlines.append(td)

    web_text = body_data.div2
    print(web_text)

    # Retrieve the parent divs for all articles
    results = soup.find_all('div')
    print(results)


    news_title = []
    div_cl = soup.find_all('div', class_="content_title")

    for title in div_cl:
        news_title.append(title.a.text[1:][:-1])
    print(news_title)

    news_p = []
    div_text = soup.find_all('div', class_="rollover_description_inner")

    for new in div_text:
        news_p.append(new.text[1:][0:-1])

    print(news_p)

    combined = list(zip(news_title, news_p))
    print(combined)
    comb_df = pd.DataFrame(combined)
    print(comb_df)

    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # Retrieve page with the requests module
    response2 = requests.get(url2)
    # Create BeautifulSoup object; parse with 'lxml'
    soup2 = bs4.BeautifulSoup(response2.text, 'lxml')


    featured_image_url = []
    pics = soup2.find_all('div', class_="img")

    for pic in pics:
        featured_image_url.append(pic.img.attrs['src'])

    print(featured_image_url)

    ###Splinter receiving erro but this finds the same picture
    alt_image =  soup2.find_all('article', class_="carousel_item")
    feat_img = alt_image[0].attrs['style'][23:-3]
    print(feat_img)

    url3 = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module
    response3 = requests.get(url3)
    # Create BeautifulSoup object; parse with 'lxml'
    soup3 = bs4.BeautifulSoup(response3.text, 'lxml')

    browser.visit('https://twitter.com/marswxreport?lang=en')

    xpath = '/html/body/div/div/div/div/main/div/div/div/div[1]/div/div/div/div/div[2]/section/div/div/div/div[1]/div/article/div/div[2]/div[2]/div[2]/span[1]'

    first_tweet = browser.find_by_xpath(xpath)[0]
    mars_weather = first_tweet.text
    print(mars_weather)

    url4 = 'https://space-facts.com/mars/'

    # Retrieve page with the requests module
    response4 = requests.get(url4)
    # Create BeautifulSoup object; parse with 'lxml'
    soup4 = bs4.BeautifulSoup(response4.text, 'lxml')
    # Set up splinter scrape
    browser.visit('https://twitter.com/marswxreport?lang=en')

    table_ele =  soup4.find_all('td')
    table_list = []
    for i in range(0,len(table_ele)):
        if (i % 2) == 0:
            print(table_ele[i].text,table_ele[i+1].text)
            table_list.append([table_ele[i].text, table_ele[i+1].text])

    mars_df = pd.DataFrame(table_list[18:],columns=["Planet:","Mars"])
    print(mars_df)

    show = mars_df.to_html('mars.htm')

    hemi_1 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    hemi_2 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    hemi_3 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    hemi_4 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'

    hemi_ls = [hemi_1, hemi_2, hemi_3, hemi_4]

    web_dict = {}
    img_url = []
    title = []

    for link in range(0, len(hemi_ls)):

        # Retrieve page with the requests module
        response = requests.get(hemi_ls[link])
        # Create BeautifulSoup object; parse with 'lxml'
        soup = bs4.BeautifulSoup(response.text, 'lxml')

        #create dictionary
        web_dict[link] = [hemi_ls[link], soup]
        links = soup.find_all('li')
        img_url.append(links[1].a.attrs['href'])
        h2_txt = soup.find_all('h2', class_='title')
        title.append(h2_txt[0].text)

    hemisphere_image_urls = []
    for i in range(0,len(title)):
        hemisphere_image_urls.append({title[i] : img_url[i]})


    ####Format data to dict
    info_dict = mars_df.to_dict('split')

    print(img_url)
    print(title)
    print(hemisphere_image_urls)

    ######THE END DICTIONARY
    mars_info = {}
    art_ls = []
    art_count = 0

    for title in news_title:
        para = news_p[art_count]
        art_ls.append({title : para})
        art_count += 1

    mars_info["news"] = art_ls
    mars_info['featured'] = feat_img
    mars_info['weather'] = mars_weather
    mars_info['table'] = info_dict
    mars_info['hemispheres'] = hemisphere_image_urls
    print(mars_info)
    x = mars_info
    return x