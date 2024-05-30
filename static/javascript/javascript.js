// document.addEventListener("DOMContentLoaded", function () {
//     var swiper = new Swiper(".swiper-container", {
//         slidesPerView: "auto",  // Show only one image at a time
//         spaceBetween: 10,
//         grabCursor: true,
//         centeredSlides: true,
//         loop: true,
//         // Additional Swiper options can be added here
//     });
// });

var swiper = new Swiper('.swiper-container', {
    direction: 'horizontal',
    slidesPerView: '1', 
    spaceBetween: 0,
    mousewheel: false,  // Enables mousewheel control
    freeMode: false,    // Makes it feel more like scrolling
    // autoplay: {
    //     delay: 2500,
    //     disableOnInteraction: false,
    // },
    pagination: {
        el: '.swiper-pagination',
        type: 'bullets',
        clickable: true,
    },
});

var swiper_highlights = new Swiper('.swiper-highlights', {
    direction: 'horizontal',
    slidesPerView: '3', 
    spaceBetween: 25,
    mousewheel: false,  // Enables mousewheel control
    freeMode: false,    // Makes it feel more like scrolling
    // autoplay: {
    //     delay: 2500,
    //     disableOnInteraction: false,
    // },
    pagination: {
        el: '.swiper-pagination',
        type: 'bullets',
        clickable: true,
    },
});




document.addEventListener("DOMContentLoaded", function() {
    var button = document.getElementById('toggle-button');
    if (button) {
        button.addEventListener('click', function() {
            var posts = document.querySelectorAll('.post.hidden');
            
            if (button.textContent === 'Load More') {
                posts.forEach(function(post) {
                    post.style.display = 'flex';
                });
                button.textContent = 'Show Less';
            } else {
                posts.forEach(function(post) {
                    post.style.display = 'none';
                });
                button.textContent = 'Load More';
            }
        });
    }
});



// lightbox
// document.addEventListener('DOMContentLoaded', function() {
//     // Add event listeners to swiper slides
//     const slides = document.querySelectorAll('.swiper-slide');
//     slides.forEach(slide => {
//         slide.addEventListener('click', function() {
//             // Show lightbox
//             document.getElementById('lightbox').style.display = 'block';

//             // You can add code here to determine whether it's an image or video and then append that to 'lightbox-media' div.
//             // Example:
//             // const media = '<img src="path-to-image">';
//             // document.getElementById('lightbox-media').innerHTML = media;
//         });
//     });

//     // Close the lightbox
//     document.getElementById('close-lightbox').addEventListener('click', function() {
//         document.getElementById('lightbox').style.display = 'none';
//     });

//     // Download actions
//     // TODO: Add your download logic here for both the 'download-single' and 'download-all' buttons
// });



document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners to swiper slides
    const slides = document.querySelectorAll('.swiper-slide');
    slides.forEach(slide => {
        slide.addEventListener('click', function(e) {
            // Reference to the parent swiper-container of the clicked slide
            const clickedSwiper = e.target.closest('.swiper-container');

            // Clone the clicked swiper container
            const clonedSwiper = clickedSwiper.cloneNode(true);

            // Insert the cloned swiper into the lightbox
            const lightboxMedia = document.getElementById('lightbox-media');
            lightboxMedia.innerHTML = ''; // Clear existing content
            lightboxMedia.appendChild(clonedSwiper);

            // Initialize a new Swiper instance for the cloned swiper container
            new Swiper(clonedSwiper, {
                direction: 'horizontal',
                slidesPerView: '1', 
                spaceBetween: 0,
                mousewheel: false,  // Enables mousewheel control
                freeMode: false,    // Makes it feel more like scrolling
                // autoplay: {
                //     delay: 2500,
                //     disableOnInteraction: false,
                // },
                pagination: {
                    el: '.swiper-pagination',
                    type: 'bullets',
                    clickable: true,
                },
            });

            // Show the lightbox
            // Get all elements with the class 'swiper-slide'
            // grid_img = document.getElementsByClassName('grid-img');
            // if(grid_img){
            //     grid_img.classList.add('lightbox-file');
            //     // grid_img.style.objectFit = 'contain';
            // }
                

            // grid_video = document.getElementsByClassName('grid-video');
            // if(grid_video){
            //     grid_video.classList.add('lightbox-file');
            // }
               



            document.getElementById('lightbox').style.display = 'block';
        });
    });

    // Close the lightbox and clear its contents
    document.getElementById('close-lightbox').addEventListener('click', function() {
        document.getElementById('lightbox').style.display = 'none';
        document.getElementById('lightbox-media').innerHTML = '';
    });

    // Download
    document.getElementById('download-all').addEventListener('click', function() {
        const activeSwiperContainer = document.querySelector('#lightbox .swiper-container');
        
        const zipId = activeSwiperContainer.getAttribute('data-id');
        if(zipId){
            const downloadUrl = `https://drive.google.com/uc?export=download&id=${zipId}`;
            window.location.href = downloadUrl;
        }
        

    });
});


function hideLoader() {
    const loader = document.getElementById('video-loader');
    loader.style.display = 'none';
}



