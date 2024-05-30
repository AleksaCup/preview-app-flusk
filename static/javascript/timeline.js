// window.addEventListener('DOMContentLoaded', (event) => {
//     const sections = document.querySelectorAll('.timeline .section');
//     const lastSection = sections[sections.length - 1];
//     if (lastSection) {
//         lastSection.classList.add('last-section');
//     }
// });


window.addEventListener('DOMContentLoaded', () => {
    let totalHeight = 0;
    const sections = document.querySelectorAll('.timeline .section');
    sections.forEach(section => {
        totalHeight += section.offsetHeight;
    });
    
    // Adding the height of the last node's circle (8px) and its top offset (-3px)
    totalHeight += 5;

    // Create a new style element to override the existing CSS
    const style = document.createElement('style');
    style.innerHTML = `
        .timeline::before {
            height: ${totalHeight}px;
        }
    `;

    // Append the style to the head of the document
    document.head.appendChild(style);
});
