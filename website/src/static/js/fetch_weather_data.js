document.addEventListener('DOMContentLoaded', function() {
    const citySelect = document.getElementById('city-select');
    const temperatureElement = document.getElementById('temperature');
    const humidityElement = document.getElementById('humidity');
    const windSpeedElement = document.getElementById('wind-speed');
    const descElement = document.getElementById('weather-desc');
    const iconElement = document.getElementById('icon');

    // Fetch weather data when the page loads with the default selected city
    fetchWeather(citySelect.value);

    // Event listener for select element
    citySelect.addEventListener('change', function() {
        const selectedCity = citySelect.value;
        fetchWeather(selectedCity);
    });

    // Function to fetch weather data from the server
    function fetchWeather(city) {
        // Make AJAX request to the server's API endpoint
        const xhr = new XMLHttpRequest();
        xhr.open('GET', 'http://localhost:5000/weather?city=' + city);
        xhr.onload = function() {
            if (xhr.status === 200) {
                const weatherData = JSON.parse(xhr.responseText);
                updateInfo(weatherData);
            } else {
                console.log('Error fetching weather data.');
            }
        };
        xhr.send();
    }

    function updateInfo(weatherData) {
        updateWeatherInfo(weatherData);
        updateDateTime();
    }

    function updateWeatherInfo(weatherData) {
        temperatureElement.textContent = weatherData.temperature + '°C';
        humidityElement.textContent = weatherData.humidity + '%';
        windSpeedElement.textContent = weatherData.wind_speed + ' m/s';
        descElement.textContent = weatherData.desc;

        const iconUrl = `https://openweathermap.org/img/wn/${weatherData.icon_code}@2x.png`;
        iconElement.src = iconUrl;
    }

    function updateDateTime() {
        /*
        Replace all default texts within the data-container div with the actual date
        The formattedDate is of following format: Wednesday, July 12, 2023 at 7:00 PM
        */ 
        const timeZone = getTimeZone();
        
        const currentDate = new Date();
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', timeZone: timeZone };
        const formattedDate = currentDate.toLocaleDateString('en-US', options);

        const day = formattedDate.split(',')[0];
        const yearAndTime = formattedDate.split(',')[2].split("a");
        const date = formattedDate.split(',')[1] + ', ' + yearAndTime[0].trim();
        const time = yearAndTime[1];
        
        const dateDaynameElement = document.querySelector('.date-dayname');
        dateDaynameElement.textContent = day;
        
        const dateDayElement = document.querySelector('.date-day');
        dateDayElement.textContent =  date;

        const dateTime = document.querySelector('.date-time');
        dateTime.textContent = "a" + time;
    }

    function getTimeZone() {
        const selectedCity = citySelect.value;
        let timeZone;
        
        if (selectedCity === 'Montreal') timeZone = "America/Montreal";
        else if (selectedCity === 'London') timeZone = "Europe/London";
        else if (selectedCity === 'Paris') timeZone = "Europe/Paris";

        return timeZone;
    }

    // Call updateDateTime every minute (60,000 milliseconds)
    setInterval(updateDateTime, 60000);

    // Call fetch Weather every ten minutes (600,000 milliseconds)
    setInterval(function() {
        const selectedCity = citySelect.value;
        fetchWeather(selectedCity);
    }, 600000);
});