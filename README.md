# Food Explorer Web Application
![food_explorer_logo](https://github.com/Joanna-Khek/food-explorer/assets/53141849/806fcdd9-cd4c-4fa8-bff4-ca764843d960)

## Project Description
Food Explorer is a web application built using Streamlit. This app will allow users to search for the best foods to explore based on the number of reviews, the number of wishlisted, and pricing per pax. At this stage, the app is focused on the Tampines area, catering to food enthusiasts and travelers looking for exciting culinary experiences in that locality. The app utilises data scraped from [Burpple](https://www.burpple.com/)

## Tools
Scraping of data: **Selenium**    
Web Application: **Python**     
To ensure reproducibility: **Docker**    

## Accessing the Web Application
**URL:** https://food-explorer.streamlit.app/     

**Docker:** To run locally using docker,

1. Clone the repository     
``git clone https://github.com/Joanna-Khek/food-explorer/``  

2. Build the docker image    
```docker build -t food-explorer:latest .```   

3. Run the docker image    
```docker run -p 8501:8501 food-explorer:latest```

4. View the web app using this url    
```http://localhost:8501/```



## Demo
1. Users can filter food choices through categories

![gif2](https://github.com/Joanna-Khek/food-explorer/assets/53141849/c0e8f255-e95c-4499-9ab3-c3e98cb8a5e6)

2. Users can sort by number of reviews, number of wishlisted and average price per pax

![gif1](https://github.com/Joanna-Khek/food-explorer/assets/53141849/267f4203-a71e-42fa-8ebe-7c7e4faf664f)

3. Users can view the summarised reviews in the form of a wordcloud and the images submitted by the reviewers

![gif3](https://github.com/Joanna-Khek/food-explorer/assets/53141849/b0a86724-2245-4448-9190-6f70b13e1ba0)

## Future Work
The web application will be updated to include more areas
