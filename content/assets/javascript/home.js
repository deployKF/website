// TODO: handle return to homepage page after navigating away (DOMContentLoaded event not firing)
document.addEventListener('DOMContentLoaded', function () {
    let words = ['Open', 'Effortless', 'Custom'];
    let currentWordIndex = 0;
    const highlightElement = document.querySelector('.mdx-hero__tag-highlight');

    function changeWord() {
        // Fade out current word (accounting for the fact there might not be a current class)
        highlightElement.classList.add('mdx-hero__tag-highlight--fade-out');

        // Change word after the fade out animation is complete
        setTimeout(() => {
            currentWordIndex = (currentWordIndex + 1) % words.length;
            highlightElement.textContent = words[currentWordIndex];

            // Fade in the new word
            highlightElement.classList.remove('mdx-hero__tag-highlight--fade-out');
        }, 500); // This timeout should match the transition duration in the CSS for the fade effect
    }

    // Change the word every 6 seconds
    setInterval(changeWord, 6000);
});