import tensorflow as tf

# Pastikan hanya CPU yang digunakan
tf.config.set_visible_devices([], 'GPU')  # Disable GPU jika terdeteksi

print("Available devices:", tf.config.list_physical_devices('CPU'))
