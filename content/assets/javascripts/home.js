let intervalId;

function startHeroAnimation() {
    // Do not start another animation if one is already running.
    if (intervalId) {
        return;
    }

    let words = ['Open', 'Effortless', 'Custom'];
    let currentWordIndex = 0;
    const highlightElement = document.querySelector('.mdx-hero__tag-highlight');

    // If there is no highlight element, do not start the animation
    if (!highlightElement) {
        console.warn('Could not find the highlight element for the hero animation.');
        return;
    }

    function changeWord() {
        // Fade out current word
        highlightElement.classList.add('mdx-hero__tag-highlight--fade-out');

        // Change word after the fade out animation is complete
        setTimeout(() => {
            currentWordIndex = (currentWordIndex + 1) % words.length;
            highlightElement.textContent = words[currentWordIndex];

            // Fade in the new word
            highlightElement.classList.remove('mdx-hero__tag-highlight--fade-out');
        }, 500); // timeout should match the transition duration in the CSS for the fade effect
    }

    // Change the word every 5 seconds
    intervalId = setInterval(changeWord, 5000);
}

function stopHeroAnimation() {
    if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
    }
}

document.addEventListener("DOMContentLoaded", function () {
    // Start the animation on page load, if we are on the homepage
    if (window.location.pathname === '/' || window.location.pathname === '') {
        startHeroAnimation();
    }

    // Listen for navigation events
    const subscription = location$.subscribe((url) => {
        // wait 1 second before starting the animation (to allow the page to load)
        setTimeout(() => {
            if (url.pathname === '/' || url.pathname === '') {
                startHeroAnimation();
            } else {
                stopHeroAnimation();
            }
        }, 1000);
    });
});