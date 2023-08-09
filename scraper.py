import requests
from bs4 import BeautifulSoup

def get_webpage_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to retrieve page. Status code: {response.status_code}")
        return None


def extract_filtered_links(content):
    soup = BeautifulSoup(content, 'html.parser')
    links = soup.find_all('a')
    
    # Filter and clean the links
    filtered_links_set = set()
    unique_filtered_links = []
    for link in links:
        if link.has_attr('href') and link['href'].startswith("https://elavegan.com/de/"):
            clean_link = link['href'].split('#')[0]  # Remove the #-part
            if clean_link not in filtered_links_set:
                filtered_links_set.add(clean_link)
                unique_filtered_links.append(clean_link)
    
    return unique_filtered_links


def is_recipe_page(link):
    content = get_webpage_content(link)
    if content and 'class="wprm-recipe-ingredients"' in content.decode('utf-8'):
        return True
    return False


def extract_recipe_details(link):
    content = get_webpage_content(link)
    if not content:
        return None
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Extract title
    title_tag = soup.find('h1', class_='entry-title')
    title = title_tag.get_text(strip=True) if title_tag else None
    
    # Extract image URL
    image_url = None
    if title_tag:  # Ensure the title tag is present
        subsequent_images = title_tag.find_all_next('img', limit=1)
        if subsequent_images:
            image_url = subsequent_images[0].get('src')
    
    # Construct the data dictionary
    recipe_data = {
        'title': title,
        'recipe_url': link,
        'image_url': image_url
    }
    
    return recipe_data



def main():
    base_url = 'https://elavegan.com/de/'
    content = get_webpage_content(base_url)
    
    if content:
        filtered_links = extract_filtered_links(content)
        for link in filtered_links:
            if is_recipe_page(link):
                recipe_data = extract_recipe_details(link)
                if recipe_data:
                    print(recipe_data)
                    # Later, you can insert this dictionary into MongoDB



if __name__ == "__main__":
    main()
