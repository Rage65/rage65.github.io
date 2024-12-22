  
    const themeCheckbox = document.querySelector('.theme-checkbox');
    const container = document.querySelector('.container');
    const text = document.querySelectorAll('h2, p'); // Select all h2 and p elements 

    themeCheckbox.addEventListener('change', () => {
      if (themeCheckbox.checked) {
        // Light mode
        container.classList.remove('dark-mode');
        container.classList.add('light-mode');
        text.forEach(element => { // Loop through each element in the NodeList
          element.classList.add('text-dark')
          element.classList.remove('text-light')
        });
      } else {
        // Dark mode
        container.classList.remove('light-mode');
        container.classList.add('dark-mode');
        text.forEach(element => {
          element.classList.add('text-light')
          element.classList.remove('text-dark')
        });
      }
    }