# BASNet HTTP

This is an HTTP service wrapper for [BASNet: Boundary-Aware Salient Object Detection code](https://github.com/NathanUA/BASNet)

It's highly recommended to run this image on a machine with a CUDA compatible Nvidia Card and minimum 6Gb of RAM.

# Development

- Clone this repository: `git clone https://github.com/cyrildiagne/BASNet-http.git`
- Go into the cloned directory: `cd BASNet-http`
- Clone the [BASNet repository](https://github.com/NathanUA/BASNet)
- Download the pretrained model [basnet.pth](https://drive.google.com/open?id=1s52ek_4YTDRt_EOkx1FS53u-vJa0c4nu)
- Put the file inside the `BASNet/saved_models/basnet_bsi/` folder.

# Usage:

### Locally with virtualenv

Requires Python v3.10+

```bash
virtualenv venv
venv/bin/activate
```

```bash
pip install torch==0.4.1
pip install -r requirements.txt
```

```
python main.py
```

The app will run on port 8080, you can change this in main.py.
