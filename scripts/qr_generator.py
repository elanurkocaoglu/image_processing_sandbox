import qrcode

def generate_n_qrs(n_qrs=5):
    for number in range(n_qrs):
        qr = qrcode.make(f"Victim #{number+1}")
        qr.save(f"./generated_qrs/victim{number+1}.png")

if __name__=="__main__":
    generate_n_qrs()