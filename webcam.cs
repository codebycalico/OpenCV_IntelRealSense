using UnityEngine;
using UnityEngine.UI;

public class WebcamDisplay : MonoBehaviour
{
    public RawImage rawImage; // Drag your RawImage component here in the Inspector
    private WebCamDevice[] devices;

    void Start()
    {
        devices = WebCamTexture.devices;
        WebCamTexture webcamTexture = new WebCamTexture(devices[1].name);
        rawImage.texture = webcamTexture;
        rawImage.material = null;
        webcamTexture.Play();
    }
}
