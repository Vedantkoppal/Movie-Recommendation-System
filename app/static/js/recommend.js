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
// const displaySimilarMovies = (movies) => {
//     const similarList = document.getElementById("similar-list");
//     similarList.innerHTML = ""; // Clear previous similar movies

//     movies.forEach(movie => {
//         // Create a container for each movie
//         const movieItem = document.createElement('div');
//         movieItem.classList.add(
//             "bg-gray-100", 
//             "rounded-lg", 
//             "shadow-sm", 
//             "px-4", 
//             "py-2", 
//             "text-gray-800", 
//             "text-m", 
//             "font-black",
//             "font-medium",
//             "flex", 
//             "items-center", 
//             "justify-center"
//         );

//         // Set the movie title
//         movieItem.textContent = movie.title;

//         // Append the movie item to the similar list container
//         similarList.appendChild(movieItem);
//     });
// };

// Function to display similar movies
const displaySimilarMovies = async (movies) => {
    const similarList = document.getElementById("similar-list");
    similarList.innerHTML = ""; // Clear previous movies    

    for (const movie of movies) {
        try {
            // Fetch movie details from Flask API
            const response = await fetch(`/api/movie?title=${encodeURIComponent(movie.title)}`);
            const movieData = await response.json();

            // Create movie card using existing structure
            const movieItem = document.createElement("div");
            movieItem.classList.add(
                "relative", "w-[250px]", "sm:w-[260px]", "md:w-[280px]", "lg:w-[300px]", "xl:w-[320px]", 
                "flex", "flex-col", "items-center"
            );

            // Image container
            const imgContainer = document.createElement("div");
            imgContainer.classList.add(
                "relative", "w-full", "h-[400px]", "sm:h-[420px]", "md:h-[440px]", "lg:h-[460px]", "xl:h-[480px]", 
                "overflow-hidden", "bg-gray-900", "flex", "items-center", "justify-center"
            );

            const imgElement = document.createElement("img");
            imgElement.src = movieData.Poster || "https://via.placeholder.com/300"; // Default image
            imgElement.alt = movieData.Title;
            imgElement.classList.add("w-full", "h-full", "object-cover");

            const overlay = document.createElement("div");
            overlay.classList.add(
                "absolute", "inset-0", "bg-black", "bg-opacity-80", "text-white", 
                "flex", "items-center", "justify-center", "opacity-0", 
                "hover:opacity-100", "transition-opacity", "duration-300", "p-4"
            );

            const plotText = document.createElement("p");
            plotText.classList.add("text-base", "text-center", "font-bold");
            plotText.style.fontFamily = "'Special Elite', monospace";
            plotText.textContent = movieData.Plot || "No plot available";

            overlay.appendChild(plotText);
            imgContainer.appendChild(imgElement);
            imgContainer.appendChild(overlay);

            // Movie title
            const titleElement = document.createElement("h2");
            titleElement.classList.add(
                "text-2xl", "sm:text-xl", "font-extrabold", "text-white", "mt-1", 
                "text-center", "w-full", "break-words", "text-green-400"
            );
            titleElement.style.fontFamily = "'monospace', sans-serif";
            titleElement.textContent = movieData.Title;

            movieItem.appendChild(imgContainer);
            movieItem.appendChild(titleElement);

            similarList.appendChild(movieItem);
        } catch (error) {
            console.error("Error fetching movie details:", error);
        }
    }
};


});
