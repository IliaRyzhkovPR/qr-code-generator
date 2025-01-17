document.addEventListener('DOMContentLoaded', function() {
    const copyLinkBtn = document.getElementById('copy-link');
    const shareFacebookBtn = document.getElementById('share-facebook');
    const shareTwitterBtn = document.getElementById('share-twitter');
    const shareLinkedInBtn = document.getElementById('share-linkedin');
    const pageQrContainer = document.getElementById('page-qr');
    const shareUrl = window.location.href; // URL to share
    const shareTitle = "Check out this QR Code Generator!";
    const shareDescription = "Create custom QR codes for your phone contacts with our easy-to-use generator.";
    const shareHashtag = "#QRCodeGenDBAX"; // Hashtag for social media sharing

    // Copy link functionality
    copyLinkBtn.addEventListener('click', function() {
        navigator.clipboard.writeText(window.location.href).then(function() {
            alert('Link copied to clipboard!');
        }, function(err) {
            console.error('Could not copy text: ', err);
        });
    });

    // Social media sharing
    shareFacebookBtn.addEventListener('click', function() {
        const fbShareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`;
        window.open(fbShareUrl, '_blank');
    });

    shareTwitterBtn.addEventListener('click', function() {
        const twitterShareUrl = `https://twitter.com/intent/tweet?url=${encodeURIComponent(shareUrl)}&text=${encodeURIComponent(shareTitle)}&hashtags=${encodeURIComponent(shareHashtag.slice(1))}`;
        window.open(twitterShareUrl, '_blank');
    });

    shareLinkedInBtn.addEventListener('click', function() {
        const linkedInShareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(shareUrl)}`;
        window.open(linkedInShareUrl, '_blank');
    });

    // Generate QR code for the page
    new QRCode(pageQrContainer, {
        text: window.location.href,
        width: 128,
        height: 128
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var modal = document.getElementById('descriptionModal');
    var closeButton = document.getElementById('closeModal');

    // Check if the user has visited before
    if (!localStorage.getItem('visitedBefore')) {
        modal.style.display = 'block';
        localStorage.setItem('visitedBefore', 'true');
    }

    // Close the modal when the button is clicked
    closeButton.onclick = function() {
        modal.style.display = 'none';
    }

    // Close the modal if the user clicks outside of it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
});