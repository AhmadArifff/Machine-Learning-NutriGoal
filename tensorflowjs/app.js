let model;

// Fungsi untuk memuat model
async function loadModel() {
    model = await tf.loadLayersModel('model/model.json');
    console.log("Model loaded successfully");
}

// Memuat model saat halaman dibuka
window.onload = async () => {
    await loadModel();
};

// Fungsi untuk menghitung BMR
function calculateBMR(weight, height, age, gender) {
    if (gender.toLowerCase() === 'pria') {
        return 66.5 + (13.75 * weight) + (5.003 * height) - (6.75 * age);
    } else {
        return 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age);
    }
}

// Fungsi untuk menghitung kebutuhan kalori harian
function calculateDailyCalories(bmr, activityLevel) {
    const factors = {
        'sedentary': 1.2,
        'lightly active': 1.375,
        'moderately active': 1.55,
        'very active': 1.725
    };
    return bmr * factors[activityLevel];
}

// Fungsi untuk prediksi kalori dan merekomendasikan makanan
async function predictCalories() {
    const weight = parseFloat(document.getElementById('weight').value);
    const height = parseFloat(document.getElementById('height').value);
    const age = parseInt(document.getElementById('age').value);
    const gender = document.getElementById('gender').value;
    const activity = document.getElementById('activity').value;

    // Hitung BMR dan kebutuhan kalori
    const bmr = calculateBMR(weight, height, age, gender);
    const dailyCalories = calculateDailyCalories(bmr, activity);
    
    // Buat input untuk model
    const input = tf.tensor2d([[dailyCalories, 50, 20, 10, 30, 15, 5, 0, 1500, 60, 100, 18, 3500]]);
    
    // Prediksi menggunakan model
    const prediction = model.predict(input);
    const predictedValues = prediction.arraySync()[0];

    // Menampilkan hasil
    document.getElementById('result').innerHTML = `
        <p><b>BMR:</b> ${bmr.toFixed(2)} kcal</p>
        <p><b>Daily Calorie Needs:</b> ${dailyCalories.toFixed(2)} kcal</p>
        <p><b>Recommended Calories:</b> ${predictedValues[0].toFixed(2)} kcal</p>
    `;
}
