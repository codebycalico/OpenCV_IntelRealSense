using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System;

public class UdpSocket : MonoBehaviour
{
    Thread receiveThread;
    UdpClient client;
    IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, 0);
    public int port = 5052;
    public bool startRecieving = true;
    public bool printToConsole = true;
    public string data;
    public string[] dataSplit;
    //public int sendPort = 5051; // Port to send to

    void Start()
    {
        // UDP Connection setup
        client = new UdpClient(port);
        receiveThread = new Thread(new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();
        Debug.Log("UDP Receiver started.");
    }

    void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            // Get the mouse position in screen space
            Vector3 mouseScreenPosition = Input.mousePosition;

            Debug.Log("Mouse clicked at: " + mouseScreenPosition);
        }
    }

    void OnDisable()
    {
        if (receiveThread != null)
        {
            receiveThread.Abort();
        }
        if (client != null)
        {
            client.Close();
        }
    }

    void ReceiveData()
    {
        while (startRecieving)
        {
            try
            {
                byte[] dataByte = client.Receive(ref anyIP);
                data = Encoding.UTF8.GetString(dataByte);
                dataSplit = data.Split(",");

                //CreateBoxCollider(dataSplit[0], dataSplit[1], dataSplit[2], dataSplit[3]);

                if (printToConsole)
                {
                    Debug.Log($"Received center X from Python: {dataSplit[0]}");
                }

                // Example: Send a response back to Python
                // byte[] response = Encoding.UTF8.GetBytes("Hello from Unity!");
                // client.Send(response, response.Length, sendIP, sendPort);
            }
            catch (System.Exception err)
            {
                Debug.LogError(err.ToString());
            }
        }
    }

    private void CreateBoxCollider(float centerX, float centerY, float width, float height)
    {
        // Get Collider component and adjust size and position based on incoming data
        // box.center = new Vector3(centerX, centerY, 0);
        // box.size = new Vector3(width, height, 0);
    }

    private void OnApplicationQuit()
    {
        if (receiveThread != null && receiveThread.IsAlive)
        {
            receiveThread.Abort();
        }
        if (client != null)
        {
            client.Close();
        }
    }

    /*// Example function to send data from Unity
    public void SendData(string message)
    {
        byte[] data = Encoding.UTF8.GetBytes(message);
        client.Send(data, data.Length, sendIP, sendPort);
        Debug.Log($"Sent to Python: {message}");
    } */
}
