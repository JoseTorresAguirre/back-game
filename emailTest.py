import smtplib
from email.mime.text import MIMEText

def enviar_correo(destinatario):
    # Configuración del correo
    remitente = "jos89.24@gmail.com"
    contraseña = 'oaho jatz tkur omwl'

    # Crear el mensaje
    mensaje = MIMEText("¡Bienvenido! Gracias por registrarte.")
    mensaje["Subject"] = "Correo de bienvenida3"
    mensaje["From"] = remitente
    mensaje["To"] = destinatario

    # Imprimir el correo del destinatario en la consola
    print("Enviando correo a:", destinatario)
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(remitente, contraseña)
        server.sendmail(remitente, destinatario, mensaje.as_string())
        server.quit()
        print("Correo enviado exitosamente", destinatario)
    except Exception as e:
        print(f"Error al enviar el correo a {destinatario}: {e}")

# Ejemplo de cómo llamar a la función
#if __name__ == '__main__':
#   email_destinatario = "45600874@certus.edu.pe"  # Puedes cambiar esto por la variable que recibas
#   enviar_correo(email_destinatario)
