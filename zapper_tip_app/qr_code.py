import qrcode
from PIL import Image

def generate_qr_code(payfast_url):
    # Create a QR code instance
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    
    # Add data to the QR code
    qr.add_data(payfast_url)
    qr.make(fit=True)
    
    # Create an image from the QR code
    img = qr.make_image(fill='black', back_color='white')
    
    # Save the image
    img.save('payfast_payment_qr.png')
    print("QR code generated and saved as 'payfast_payment_qr.png'.")
    
    # Display the QR code
    img.show()

# Example usage
if __name__ == "__main__":
    example_url = "https://sandbox.payfast.co.za/eng/process?merchant_id=10035640&merchant_key=njtokoc5074bx&amount=100&item_name=Tip%20Payment"
    generate_qr_code(example_url)