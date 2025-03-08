// Initialize AOS (Animate On Scroll)
AOS.init({
     duration: 1000,
     once: true
 });
 
 // Input Type Switcher
 const inputTypes = document.querySelectorAll('.input-type');
 inputTypes.forEach(button => {
     button.addEventListener('click', () => {
         document.querySelector('.input-type.active').classList.remove('active');
         button.classList.add('active');
         
         const type = button.dataset.type;
         document.querySelectorAll('[data-content]').forEach(element => {
             element.classList.remove('active');
         });
         document.querySelector(`[data-content="${type}"]`).classList.add('active');
     });
 });
 
 // Drag & Drop functionality
 const uploadArea = document.querySelector('.upload-area');
 const fileInput = document.querySelector('#fileInput');
 const results = document.querySelector('.results');
 
 uploadArea.addEventListener('click', () => fileInput.click());
 
 uploadArea.addEventListener('dragover', (e) => {
     e.preventDefault();
     uploadArea.style.borderColor = '#009FFD';
 });
 
 uploadArea.addEventListener('dragleave', () => {
     uploadArea.style.borderColor = '#2A2A72';
 });
 
 uploadArea.addEventListener('drop', (e) => {
     e.preventDefault();
     handleFile(e.dataTransfer.files[0]);
 });
 
 fileInput.addEventListener('change', (e) => handleFile(e.target.files[0]));
 
 // Text Analysis Function
 function analyzeText() {
     const text = document.getElementById('newsText').value;
     if (!text.trim()) {
         alert('Please enter some text to analyze');
         return;
     }
 
     // Simulate analysis
     results.classList.add('visible');
     results.innerHTML = `
         <h3>Analysis Results</h3>
         <div class="result-item">
             <p>Credibility Score: <span class="score">${Math.floor(Math.random() * 40 + 60)}% Reliable</span></p>
             <div class="progress-bar">
                 <div class="progress" style="width: ${Math.floor(Math.random() * 40 + 60)}%"></div>
             </div>
         </div>
         <div class="result-item">
             <p>Key Phrases Detected: <span class="verified">${Math.floor(Math.random() * 5 + 3)} suspicious phrases found</span></p>
         </div>
         <div class="result-item">
             <p>Sentiment Analysis: <span class="verified">${Math.random() > 0.5 ? 'Neutral' : 'Biased'}</span></p>
         </div>
     `;
     
     // Scroll to results
     results.scrollIntoView({ behavior: 'smooth' });
 }
 
 // File Analysis Function
 function handleFile(file) {
     // Simulate analysis
     results.classList.add('visible');
     results.innerHTML = `
         <h3>Analysis Results</h3>
         <div class="result-item">
             <p>Credibility Score: <span class="score">85% Reliable</span></p>
             <div class="progress-bar">
                 <div class="progress" style="width: 85%"></div>
             </div>
         </div>
         <div class="result-item">
             <p>Source Verification: <span class="verified">Verified Publisher</span></p>
         </div>
     `;
     results.scrollIntoView({ behavior: 'smooth' });
 }