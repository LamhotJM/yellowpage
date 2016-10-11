## Installation
* pip install virtualenv
* virtualenv env
* env/scripts/activate
* pip install -r requirements.txt

## Running
* scrapy crawl category  (crawl list all categories)
* scrapy crawl yellowpages (crawl list of companies data)

## Logic

```json
initialize baseUrl <- yellowpage url 
foreach baseUrl as categories  
       foreach categories as subCategories 
             foreach categories as linkSubCategories 
                  linkSubCategories as paginationPage  
``` 
             