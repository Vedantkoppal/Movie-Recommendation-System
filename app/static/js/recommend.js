document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("search-input");
    const selectedList = document.getElementById("selected-list");
    const getSimilarBtn = document.getElementById("get-similar-btn");
    const selectedMovies = [];

    // Function to create suggestion box if not already present
    const createSuggestionBox = () => {
        const box = document.createElement("div");
        box.id = "suggestion-box";
        box.classList.add("absolute", "bg-white", "border", "border-gray-300", "rounded", "w-80", "mt-2", "hidden", "z-10");
        searchInput.parentElement.appendChild(box);
        return box;
    };

    // Show suggestions only if there is input
    let debounceTimer;

    searchInput.addEventListener('input', () => {
        clearTimeout(debounceTimer); // Clear the previous timer
    
        const query = searchInput.value.trim();
        if (!query) {
            hideSuggestions(); // Hide suggestions when input is empty
            return;
        }
    
        let suggestionBox = document.getElementById('suggestion-box');
        if (!suggestionBox) {
            suggestionBox = createSuggestionBox();
        }
        suggestionBox.style.display = 'block';
    
        // Delay request by 1 second (1000 ms)
        debounceTimer = setTimeout(async () => {
            const response = await fetch(`/search?q=${query}`);
            const suggestions = await response.json();
            showSuggestions(suggestions);
        }, 1000);
    });
    
    function hideSuggestions() {
        const suggestionBox = document.getElementById('suggestion-box');
        if (suggestionBox) {
            suggestionBox.style.display = 'none';
        }
    }
    

    // Function to display suggestions
    const showSuggestions = (suggestions) => {
        const suggestionBox = document.getElementById('suggestion-box');
        suggestionBox.innerHTML = ""; // Clear previous suggestions

        suggestions.forEach(movie => {
            const suggestionItem = document.createElement("div");
            suggestionItem.textContent = movie.title;
            suggestionItem.classList.add("p-2", "cursor-pointer");

            suggestionItem.addEventListener('click', () => {
                selectMovie(movie);
            });
            suggestionBox.appendChild(suggestionItem);
        }); 
    };

    // Function to select a movie
    const selectMovie = (movie) => {
        // Add movie to selected list
        selectedMovies.push(movie);
        // Update selected list in the UI
        const listItem = document.createElement('li');
        listItem.textContent = movie.title;
        listItem.classList.add('bg-teal-100', 'p-2', 'rounded', 'text-teal-700', 'text-sm');  // Tailwind styling
        selectedList.appendChild(listItem);

        // Hide suggestion box and reset input
        const suggestionBox = document.getElementById('suggestion-box');
        if (suggestionBox) {
            suggestionBox.style.display = 'none'; // Hide suggestion box after selection
        }
        searchInput.value = ""; // Reset the search input field
    };

    // Fetch similar movies on "Get Similar Movies" button click
    getSimilarBtn.addEventListener('click', async () => {
        if (selectedMovies.length > 0) {
            const movieIds = selectedMovies.map(movie => movie.id);
            const response = await fetch('/get-similar-movies', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ movie_ids: movieIds }),
            });
            const similarMovies = await response.json();
            displaySimilarMovies(similarMovies);
        }
    });

    // Function to display similar movies
const displaySimilarMovies = (movies) => {
    const similarList = document.getElementById("similar-list");
    similarList.innerHTML = ""; // Clear previous similar movies

    movies.forEach(movie => {
        // Create a container for each movie
        const movieItem = document.createElement('div');
        movieItem.classList.add(
            "bg-gray-100", 
            "rounded-lg", 
            "shadow-sm", 
            "px-4", 
            "py-2", 
            "text-gray-800", 
            "text-m", 
            "font-black",
            "font-medium",
            "flex", 
            "items-center", 
            "justify-center"
        );

        // Set the movie title
        movieItem.textContent = movie.title;

        // Append the movie item to the similar list container
        similarList.appendChild(movieItem);
    });
};

});
