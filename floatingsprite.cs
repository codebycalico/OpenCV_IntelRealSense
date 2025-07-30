using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using UnityEngine.UI;

public class FloatingSprites : MonoBehaviour
{
    public float noiseScale = 1f;
    public float speed = .3f;
    public float followSpeed = 2f;
    public float followDuration = 2f; // How long to follow after contact
    public float bufferDuration = 2f; // How long to rest before being able to follow again

    private Vector2 noiseOffset;
    private Vector2 velocity;
    private Transform target;

    private bool isFollowing = false;
    private bool isInBuffer = false;

    private float followTimer = 0f;
    private float bufferTimer = 0f;

    private List<GameObject> currentBlobs = new List<GameObject>();
    private BlobDetection blobDetect;

    void Start()
    {
        blobDetect = FindObjectOfType<BlobDetection>();

        noiseOffset = new Vector2(Random.Range(0f, 100f), Random.Range(0f, 100f));

        GameObject targetObj = GameObject.FindGameObjectWithTag("Blob");
        if (targetObj != null)
        {
            target = targetObj.transform;
        }
    }

    void Update() {
        //currentBlobs = blobDetect.getBlobs();

        if (isFollowing)
        {
            followTimer -= Time.deltaTime;

            if (followTimer <= 0f)
            {
                isFollowing = false; // Stop following
                isInBuffer = true;
                bufferTimer = bufferDuration;
            } else {
                // Follow the target
                if(target != null) {
                    Vector2 direction = (target.position - transform.position).normalized;
                    velocity = direction * followSpeed;
                }
            }
        } else {
            if(isInBuffer)
            {
                bufferTimer -= Time.deltaTime;

                if(bufferTimer <= 0f)
                {
                    isInBuffer = false; // buffer time done
                }
            }

            // Perlin noise movement
            float noiseX = Mathf.PerlinNoise(Time.time * noiseScale + noiseOffset.x, noiseOffset.y);
            float noiseY = Mathf.PerlinNoise(noiseOffset.x, Time.time * noiseScale + noiseOffset.y);
            Vector2 direction = new Vector2(noiseX - 0.5f, noiseY - 0.5f).normalized;
            velocity = direction * speed;
        }

        transform.Translate(velocity * Time.deltaTime);
    }

    void OnTriggerEnter2D(Collider2D other)
    {
        if (other.CompareTag("Blob"))
        {
            if(!isInBuffer)
            {
                isFollowing = true;
                followTimer = followDuration;
            }
        }
    }
    /*
        public float noiseScale = 1f;
        public float speed = 1f;
        public float followSpeed = 2f;
        public float followDistance = .001f; // Distance threshold to start following

        private Vector2 noiseOffset;
        private Vector2 velocity;

        private Transform target; // The object to follow, should have a circle collider
        private Vector2 startPosition;

        void Start()
        {
            noiseOffset = new Vector2(Random.Range(0f, 100f), Random.Range(0f, 100f));
            startPosition = transform.position;

            // Find a GameObject tagged "Blob"
            GameObject targetObj = GameObject.FindGameObjectWithTag("Blob");
            if (targetObj != null)
            {
                target = targetObj.transform;
            }
        }

        void Update()
        {
            if (target != null && Vector2.Distance(transform.position, target.position) < followDistance)
            {
                // Follow the target
                Vector2 direction = (target.position - transform.position).normalized;
                velocity = direction * followSpeed;
            }
            else
            {
                // Perlin noise movement
                float noiseX = Mathf.PerlinNoise(Time.time * noiseScale + noiseOffset.x, noiseOffset.y);
                float noiseY = Mathf.PerlinNoise(noiseOffset.x, Time.time * noiseScale + noiseOffset.y);
                Vector2 direction = new Vector2(noiseX - 0.5f, noiseY - 0.5f).normalized;

                velocity = direction * speed;
            }

            transform.Translate(velocity * Time.deltaTime);
        }
        _______
            public float speed = 1.3f;          // Overall speed multiplier
            public float noiseScale = 0.3f;    // Smoothness of motion (lower = smoother)
            public float offsetRange = 1000f;  // Range to randomize per-object drift
            public float repulsionForce = 5f;
            public float bounceForce = 10f;

            private Vector2 noiseOffset;
            private Rigidbody2D rb;
            private Vector2 currentDirection = new Vector2();

            void Start()
            {
                // Give each object a unique offset in Perlin noise space
                noiseOffset = new Vector2(Random.Range(0f, offsetRange), Random.Range(0f, offsetRange));
                rb = GetComponent<Rigidbody2D>();
                if (rb == null)
                {
                    Debug.LogWarning("No Rigidbody2D found on " + gameObject.name);
                }
            }

            void FixedUpdate()
            {
                float t = Time.time;

                // Get smooth pseudo-random values between 0 and 1
                float xNoise = Mathf.PerlinNoise(noiseOffset.x, t * noiseScale);
                float yNoise = Mathf.PerlinNoise(noiseOffset.y, t * noiseScale);

                // Convert to [-1, 1] range
                float xDir = (xNoise - 0.5f) * 2f;
                float yDir = (yNoise - 0.5f) * 2f;

                currentDirection.x = xDir;
                currentDirection.y = yDir;

                // Apply drift
                //Vector3 drift = new Vector3(xDir, yDir, 0f) * speed * Time.deltaTime;

                //transform.localPosition += drift;

                // Set velocity instead of transform.position to work with the collision
                Vector2 targetVelocity = new Vector2(xDir, yDir) * speed;

                if (rb != null)
                {
                    // Calculate difference between target and current velocity
                    Vector2 velocityChange = targetVelocity - rb.linearVelocity;

                    // Apply force proportional to the difference
                    rb.AddForce(velocityChange * rb.mass / Time.fixedDeltaTime);
                }
            }
            */
}

// wild 
/*
 using UnityEngine;

[RequireComponent(typeof(Rigidbody2D))]
public class FloatingSprites : MonoBehaviour
{
    public float driftForce = 1.5f;       // How much force to apply toward Perlin drift
    public float noiseScale = 0.3f;       // Smoother movement
    public float offsetRange = 1000f;     // Unique offset per sprite

    private Vector2 noiseOffset;
    private Rigidbody2D rb;

    void Start()
    {
        noiseOffset = new Vector2(Random.Range(0f, offsetRange), Random.Range(0f, offsetRange));
        rb = GetComponent<Rigidbody2D>();

        // Boost bounce by increasing mass and bounciness (optional, physics-based)
        rb.mass = 2f; // More mass = stronger bounce response (tweak as needed)
        rb.sharedMaterial = new PhysicsMaterial2D("Bouncy") {
            bounciness = 1f,
            friction = 0f
        };
    }

    void FixedUpdate()
    {
        float t = Time.time;

        float xNoise = Mathf.PerlinNoise(noiseOffset.x, t * noiseScale);
        float yNoise = Mathf.PerlinNoise(noiseOffset.y, t * noiseScale);

        float xDir = (xNoise - 0.5f) * 2f;
        float yDir = (yNoise - 0.5f) * 2f;

        Vector2 targetDirection = new Vector2(xDir, yDir).normalized;

        if (rb != null)
        {
            // Add a small force toward the target drift direction
            rb.AddForce(targetDirection * driftForce, ForceMode2D.Force);
        }
    }
}
*/

