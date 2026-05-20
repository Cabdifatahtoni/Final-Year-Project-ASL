document.addEventListener("DOMContentLoaded", function () {
    const revealElements = document.querySelectorAll(".reveal-up, .reveal-left, .reveal-right");

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (!entry.isIntersecting) return;

            entry.target.classList.add("is-visible");

            const statNumbers = entry.target.querySelectorAll(".project-stat span");
            statNumbers.forEach((numberElement) => {
                animateStatNumber(numberElement);
            });

            observer.unobserve(entry.target);
        });
    }, {
        threshold: 0.25
    });

    revealElements.forEach((el) => observer.observe(el));

    const statsSection = document.querySelector(".project-stats");

    if (statsSection) {
        const statsObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;

                const statNumbers = statsSection.querySelectorAll(".project-stat span");
                statNumbers.forEach((numberElement) => {
                    animateStatNumber(numberElement);
                });

                statsObserver.unobserve(statsSection);
            });
        }, {
            threshold: 0.35
        });

        statsObserver.observe(statsSection);
    }

    function animateStatNumber(element) {
        if (element.dataset.animated === "true") return;

        const originalText = element.textContent.trim();

        let targetNumber;
        let suffix = "";
        let useComma = false;

        if (originalText.includes(",")) {
            useComma = true;
            targetNumber = parseInt(originalText.replace(",", ""), 10);
        } else if (originalText.includes("%")) {
            suffix = "%";
            targetNumber = parseInt(originalText.replace("%", ""), 10);
        } else {
            targetNumber = parseInt(originalText, 10);
        }

        if (isNaN(targetNumber)) return;

        element.dataset.animated = "true";

        let start = 1;
        const duration = 1200;
        const startTime = performance.now();

        function updateNumber(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            const easedProgress = 1 - Math.pow(1 - progress, 3);
            const currentValue = Math.round(start + (targetNumber - start) * easedProgress);

            let displayValue = currentValue.toString();

            if (useComma) {
                displayValue = currentValue.toLocaleString();
            }

            element.textContent = displayValue + suffix;

            if (progress < 1) {
                requestAnimationFrame(updateNumber);
            } else {
                element.textContent = originalText;
            }
        }

        requestAnimationFrame(updateNumber);
    }

    const videoInput = document.getElementById("videoInput");
    const videoPreview = document.getElementById("videoPreview");
    const uploadForm = document.getElementById("uploadForm");

    if (videoInput && videoPreview) {
        videoInput.addEventListener("change", function () {
            const file = this.files[0];

            if (!file) {
                videoPreview.hidden = true;
                videoPreview.removeAttribute("src");
                return;
            }

            const videoURL = URL.createObjectURL(file);
            videoPreview.src = videoURL;
            videoPreview.hidden = false;
        });
    }

    if (uploadForm) {
        uploadForm.addEventListener("submit", function () {
            const button = uploadForm.querySelector("button");

            if (button) {
                button.textContent = "Classifying...";
                button.disabled = true;
            }
        });
    }
});