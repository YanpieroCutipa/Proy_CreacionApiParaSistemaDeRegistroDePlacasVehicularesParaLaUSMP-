// Convierte un archivo de imagen a formato base64 (Data URL)
function convertirImagenADataURL(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(reader.result); // Retorna el resultado al terminar
    reader.onerror = reject;
    reader.readAsDataURL(file); // Lee el archivo como Data URL
  });
}

// Envía la imagen seleccionada al servidor para reconocimiento de placa
async function enviarImagen() {
  const input = document.getElementById('fileInput');
  if (!input.files.length) {
    alert('Selecciona una imagen primero');
    return;
  }

  const base64 = await convertirImagenADataURL(input.files[0]); // Convierte imagen a base64

  // Realiza una solicitud POST al backend con la imagen codificada
  fetch('http://127.0.0.1:5000/api/read-plate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image_base64: base64 }) // Envía la imagen en el cuerpo de la petición
  })
  .then(res => res.json()) // Procesa la respuesta del servidor
  .then(data => {
    // Muestra el resultado en el HTML
    document.getElementById('resultado').textContent = JSON.stringify(data, null, 2);
  })
  .catch(err => {
    // Muestra errores en caso de fallo
    document.getElementById('resultado').textContent = 'Error: ' + err;
  });
}
