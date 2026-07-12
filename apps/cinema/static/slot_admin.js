document.addEventListener("DOMContentLoaded", () => {

    const movie = document.getElementById("id_movie");
    const language = document.getElementById("id_language");

    if (!movie || !language) return;

    movie.addEventListener("change", async () => {

        const movieId = movie.value;

        language.innerHTML = "";

        if (!movieId)
            return;

        const response = await fetch(`/api/movies/${movieId}/languages/`);

        const data = (await response.json()).results;

        data.forEach(lang => {

            const option = document.createElement("option");

            option.value = lang.id;
            option.textContent = lang.language;

            language.appendChild(option);

        });

    });
});
