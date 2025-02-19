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
        suggestionBox.classList.add('hidden');

        if (suggestions.length === 0) {
            hideSuggestions(); // Hide suggestion box if no suggestions
            return;
        }

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

    //  Function to display similar movies using the existing container in your HTML
    // const displaySimilarMovies = async (movies) => {
    // // Get the container already present in your HTML
    // const similarList = document.getElementById("similar-list");
    // // Clear previous similar movies
    // similarList.innerHTML = "";

    // for (const movie of movies) {
    //     try {
    //     // Fetch movie details from Flask API
    //     const response = await fetch(`/api/movie?title=${encodeURIComponent(movie.title)}`);
    //     const movieData = await response.json();

    //     // Create individual movie card container with responsive widths and flex column
    //     const movieDiv = document.createElement("div");
    //     movieDiv.classList.add(
    //         "relative",
    //         "w-[250px]",    // width on extra-small screens
    //         "sm:w-[260px]", // width on small screens
    //         "md:w-[280px]", // width on medium screens
    //         "lg:w-[300px]", // width on large screens
    //         "xl:w-[320px]", // width on extra-large screens
    //         "flex",
    //         "flex-col",
    //         "items-center",
    //         "mx-auto",
    //         "gap-4"

    //     );

    //     // Create image container with fixed heights and background styling
    //     const imgContainer = document.createElement("div");
    //     imgContainer.classList.add(
    //         "relative",
    //         "w-full",
    //         "h-[400px]",    // height on extra-small screens
    //         "sm:h-[420px]", // height on small screens
    //         "md:h-[440px]", // height on medium screens
    //         "lg:h-[460px]", // height on large screens
    //         "xl:h-[480px]", // height on extra-large screens
    //         "overflow-hidden",
    //         "bg-gray-900",
    //         "flex",
    //         "items-center",
    //         "justify-center"
    //     );

    //     // Create the image element
    //     const imgElement = document.createElement("img");
    //     imgElement.src = movieData.Poster || "https://via.placeholder.com/300";
    //     imgElement.alt = movieData.Title;
    //     imgElement.classList.add("w-full", "h-full", "object-cover");

    //     // Create overlay container for movie plot (hidden by default; appears on hover)
    //     const overlay = document.createElement("div");
    //     overlay.classList.add(
    //         "absolute",
    //         "inset-0",
    //         "bg-black",
    //         "bg-opacity-80",
    //         "text-white",
    //         "flex",
    //         "items-center",
    //         "justify-center",
    //         "opacity-0",
    //         "hover:opacity-100",
    //         "transition-opacity",
    //         "duration-300",
    //         "p-4"
    //     );

    //     // Create the paragraph element for the movie plot
    //     const plotText = document.createElement("p");
    //     plotText.classList.add("text-base", "text-center", "font-bold");
    //     plotText.style.fontFamily = "'Special Elite', monospace";
    //     plotText.textContent = movieData.Plot || "No plot available";

    //     overlay.appendChild(plotText);
    //     imgContainer.appendChild(imgElement);
    //     imgContainer.appendChild(overlay);

    //     // Create the movie title element
    //     const titleElement = document.createElement("h2");
    //     titleElement.classList.add(
    //         "text-2xl",
    //         "sm:text-xl",
    //         "font-extrabold",
    //         "text-white",
    //         "mt-1",
    //         "text-center",
    //         "w-full",
    //         "break-words",
    //         "text-green-400"
    //     );
    //     titleElement.style.fontFamily = "'monospace', sans-serif";
    //     titleElement.textContent = movieData.Title;

    //     // Assemble the movie card
    //     movieDiv.appendChild(imgContainer);
    //     movieDiv.appendChild(titleElement);

    //     // Append movie card to the existing similar movies container
    //     similarList.appendChild(movieDiv);
    //     } catch (error) {
    //     console.error("Error fetching movie details:", error);
    //     }
    // }
    // };

    
    // const displaySimilarMovies = async (movies) => {
    //     // Get the container already present in your HTML
    //     const similarList = document.getElementById("similar-list");
    //     // Clear previous similar movies
    //     similarList.innerHTML = "";
        
    //     // Apply grid container classes as in your HTML template.
    //     // These classes center the grid and add responsive spacing.
    //     similarList.className =
    //     "grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-4 gap-4 gap-y-8 mx-auto justify-items-center px-4 sm:px-6 lg:px-12";
      
    //     for (const movie of movies) {
    //       try {
    //         // Fetch movie details from Flask API
    //         const response = await fetch(`/api/movie?title=${encodeURIComponent(movie.title)}`);
    //         const movieData = await response.json();
      
    //         // Create individual movie card container.
    //         // Instead of fixed widths, we use w-full with a max-width so the card scales fluidly.
    //         const movieDiv = document.createElement("div");
    //         movieDiv.className =
    //           "relative w-full max-w-[320px] flex flex-col items-center";
      
    //         // Create image container using an aspect ratio.
    //         // This ensures the height adjusts proportionally to the width.
    //         const imgContainer = document.createElement("div");
    //         imgContainer.className =
    //           "relative w-full aspect-[2/3] overflow-hidden bg-gray-900 flex items-center justify-center";
      
    //         // Create the image element.
    //         const imgElement = document.createElement("img");
    //         imgElement.src = movieData.Poster || "https://via.placeholder.com/300";
    //         imgElement.alt = movieData.Title;
    //         imgElement.className = "w-full h-full object-cover";
      
    //         // Create overlay container for the movie plot (hidden by default; appears on hover).
    //         const overlay = document.createElement("div");
    //         overlay.className =
    //           "absolute inset-0 bg-black bg-opacity-80 text-white flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity duration-300 p-4";
      
    //         // Create the paragraph element for the movie plot.
    //         const plotText = document.createElement("p");
    //         plotText.className = "text-base text-center font-bold";
    //         plotText.style.fontFamily = "'Special Elite', monospace";
    //         plotText.textContent = movieData.Plot || "No plot available";
      
    //         overlay.appendChild(plotText);
    //         imgContainer.appendChild(imgElement);
    //         imgContainer.appendChild(overlay);
      
    //         // Create the movie title element.
    //         const titleElement = document.createElement("h2");
    //         titleElement.className =
    //           "text-2xl sm:text-xl font-extrabold text-white mt-1 text-center w-full break-words text-green-400";
    //         titleElement.style.fontFamily = "'monospace', sans-serif";
    //         titleElement.textContent = movieData.Title;
      
    //         // Assemble the movie card.
    //         movieDiv.appendChild(imgContainer);
    //         movieDiv.appendChild(titleElement);
      
    //         // Append movie card to the grid container.
    //         similarList.appendChild(movieDiv);
    //       } catch (error) {
    //         console.error("Error fetching movie details:", error);
    //       }
    //     }
    //   };
      

    //  New funciton 
    const displaySimilarMovies = async (movies) => {
        const similarList = document.getElementById("similar-list");
        similarList.innerHTML = "";
        similarList.className =
            "grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-4 gap-4 gap-y-8 mx-auto justify-items-center px-4 sm:px-6 lg:px-12";
    
        // Create an array of promises for all movie fetches
        const moviePromises = movies.map(movie =>
            fetch(`/api/movie?title=${encodeURIComponent(movie.title)}`).then(res => res.json())
        );
    
        try {
            // Wait for all requests to finish in parallel
            const movieDataArray = await Promise.all(moviePromises);
    
            movieDataArray.forEach((movieData) => {
                const movieDiv = document.createElement("div");
                movieDiv.className = "relative w-full max-w-[320px] flex flex-col items-center";
    
                const imgContainer = document.createElement("div");
                imgContainer.className = "relative w-full aspect-[2/3] overflow-hidden bg-gray-900 flex items-center justify-center";
    
                const imgElement = document.createElement("img");
                imgElement.src = movieData.Poster || "https://via.placeholder.com/300";
                imgElement.alt = movieData.Title;
                imgElement.className = "w-full h-full object-cover";
    
                const overlay = document.createElement("div");
                overlay.className = "absolute inset-0 bg-black bg-opacity-80 text-white flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity duration-300 p-4";
    
                const plotText = document.createElement("p");
                plotText.className = "text-base text-center font-bold";
                plotText.style.fontFamily = "'Special Elite', monospace";
                plotText.textContent = movieData.Plot || "No plot available";
    
                overlay.appendChild(plotText);
                imgContainer.appendChild(imgElement);
                imgContainer.appendChild(overlay);
    
                const titleElement = document.createElement("h2");
                titleElement.className = "text-2xl sm:text-xl font-extrabold text-white mt-1 text-center w-full break-words text-green-400";
                titleElement.style.fontFamily = "'monospace', sans-serif";
                titleElement.textContent = movieData.Title;
    
                movieDiv.appendChild(imgContainer);
                movieDiv.appendChild(titleElement);
                similarList.appendChild(movieDiv);
            });
        } catch (error) {
            console.error("Error fetching movie details:", error);
        }
    };
    
      

});
