let selectedCityRef = '';

document.addEventListener("DOMContentLoaded", function () {
    const cityInput = document.getElementById('city-input');
    const warehouseInput = document.getElementById('warehouse-input');

    function createDropdown(input, list) {
        let dropdown = document.createElement('div');
        dropdown.classList.add('autocomplete-dropdown');
        dropdown.style.position = 'absolute';
        dropdown.style.background = '#fff';
        dropdown.style.border = '1px solid #ccc';
        dropdown.style.borderRadius = '10px';
        dropdown.style.zIndex = '1000';
        dropdown.style.width = input.offsetWidth + 'px';

        list.forEach(item => {
            let option = document.createElement('div');
            option.textContent = item.label;
            option.style.padding = '10px';
            option.style.cursor = 'pointer';
            option.style.borderBottom = '1px solid #eee';

            option.addEventListener('click', () => {
                input.value = item.label;
                if (input === cityInput) {
                    selectedCityRef = item.ref;
                }

                dropdown.remove();
            });

            dropdown.appendChild(option);
        });

        const rect = input.getBoundingClientRect();
        dropdown.style.top = (window.scrollY + rect.bottom) + 'px';
        dropdown.style.left = rect.left + 'px';

        document.body.appendChild(dropdown);

        document.addEventListener('click', function onClickOutside(e) {
            if (!dropdown.contains(e.target) && e.target !== input) {
                dropdown.remove();
                document.removeEventListener('click', onClickOutside);
            }
        });
    }

    function debounce(func, wait) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }

    cityInput.addEventListener('input', debounce(function () {
        fetch(`/ajax/cities/?q=${encodeURIComponent(cityInput.value)}`)
            .then(res => res.json())
            .then(data => {
                document.querySelectorAll('.autocomplete-dropdown').forEach(el => el.remove());
                if (data.length) createDropdown(cityInput, data);
            });
    }, 300));

    warehouseInput.addEventListener('input', debounce(function () {
        if (!selectedCityRef) return;
        fetch(`/ajax/warehouses/?city_ref=${selectedCityRef}&q=${encodeURIComponent(warehouseInput.value)}`)
            .then(res => res.json())
            .then(data => {
                document.querySelectorAll('.autocomplete-dropdown').forEach(el => el.remove());
                if (data.length) createDropdown(warehouseInput, data);
            });
    }, 300));
});