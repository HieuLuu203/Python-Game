using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class cod_player : MonoBehaviour
{
    public float speedPlayer = 0.5f;
    private Rigidbody2D rb;
    public int jumpForce = 10;
    public bool isGround = false;
    public bool isPress = false;
    public float speedRotation;
    // Start is called before the first frame update
    void Start()
    {
        rb = gameObject.GetComponent<Rigidbody2D>();
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetMouseButtonDown(0) && !isGround) {
            isGround = true;
            rb.velocity = Vector3.zero;
            rb.AddForce(Vector2.up * jumpForce);
        }

        if (isGround)
        {
            transform.Rotate(Vector3.back * speedRotation * Time.deltaTime);
        }
    }

    private void OnCollisionEnter2D(Collision2D collision)
    {
        if (collision.gameObject.CompareTag("Ground"))
        {
            isGround = false;
        }
    }
}
