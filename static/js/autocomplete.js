// static/js/autocomplete.js - Drug name auto-suggest
class DrugAutocomplete {
    constructor(inputElement) {
        this.input = inputElement;
        this.container = document.createElement('div');
        this.container.className = 'autocomplete-container';
        this.input.parentNode.appendChild(this.container);
        
        this.bindEvents();
    }
    
    bindEvents() {
        let timeout;
        this.input.addEventListener('input', (e) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                this.search(e.target.value);
            }, 300);
        });
        
        document.addEventListener('click', (e) => {
            if (!this.container.contains(e.target) && e.target !== this.input) {
                this.hide();
            }
        });
    }
    
    async search(query) {
        if (query.length < 2) {
            this.hide();
            return;
        }
        
        try {
            const response = await fetch(`/api/drug-suggest?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            if (data.success && data.suggestions.length > 0) {
                this.show(data.suggestions);
            } else {
                this.hide();
            }
        } catch (error) {
            console.error('Autocomplete error:', error);
            this.hide();
        }
    }
    
    show(suggestions) {
        this.container.innerHTML = '';
        this.container.className = 'autocomplete-container active';
        
        suggestions.forEach(suggestion => {
            const item = document.createElement('div');
            item.className = 'autocomplete-item';
            item.textContent = suggestion.name;
            item.dataset.value = suggestion.name;
            
            if (suggestion.type) {
                const type = document.createElement('span');
                type.className = 'autocomplete-type';
                type.textContent = suggestion.type;
                item.appendChild(type);
            }
            
            item.addEventListener('click', () => {
                this.input.value = suggestion.name;
                this.input.focus();
                this.hide();
                
                if (window.MedChecker && window.MedChecker.check) {
                    window.MedChecker.check(this.input);
                }
            });
            
            this.container.appendChild(item);
        });
    }
    
    hide() {
        this.container.className = 'autocomplete-container';
        this.container.innerHTML = '';
    }
}

function initializeAutocomplete() {
    document.querySelectorAll('.med-name').forEach(input => {
        new DrugAutocomplete(input);
    });
}

window.DrugAutocomplete = DrugAutocomplete;
window.initializeAutocomplete = initializeAutocomplete;

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeAutocomplete);
} else {
    initializeAutocomplete();
}