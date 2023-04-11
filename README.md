# BASNet HTTP

This is an HTTP service wrapper for [BASNet: Boundary-Aware Salient Object Detection code](https://github.com/NathanUA/BASNet)

It's highly recommended to run this image on a machine with a CUDA compatible Nvidia Card and minimum 6GB of RAM.

# Development

- Clone this repository: `git clone https://github.com/anojht/basnet-http.git`
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

**The app will run on port 8080, you can change this in main.py.**

## Thanks and Acknowledgements

- [Original Repo](https://github.com/cyrildiagne/basnet-http) for serving as an excellent base to improve upon
- [AR Cut & Paste](https://github.com/cyrildiagne/ar-cutpaste) for serving as a reference to guide my specific implementation
- [My AR Cut & Paste for IAT359 Course Project](https://github.com/anojht/ar-cutpaste) for serving as a reference to guide my specific implementation
- [BASNet code](https://github.com/NathanUA/BASNet) for '[_BASNet: Boundary-Aware Salient Object Detection_](http://openaccess.thecvf.com/content_CVPR_2019/html/Qin_BASNet_Boundary-Aware_Salient_Object_Detection_CVPR_2019_paper.html) [code](https://github.com/NathanUA/BASNet)', [Xuebin Qin](https://webdocs.cs.ualberta.ca/~xuebin/), [Zichen Zhang](https://webdocs.cs.ualberta.ca/~zichen2/), [Chenyang Huang](https://chenyangh.com/), [Chao Gao](https://cgao3.github.io/), [Masood Dehghan](https://sites.google.com/view/masoodd) and [Martin Jagersand](https://webdocs.cs.ualberta.ca/~jag/)
- RunwayML for the [Photoshop paste code](https://github.com/runwayml/RunwayML-for-Photoshop/blob/master/host/index.jsx)
- [CoreWeave](https://www.coreweave.com) for hosting the public U^2Net model endpoint on Tesla V100s
