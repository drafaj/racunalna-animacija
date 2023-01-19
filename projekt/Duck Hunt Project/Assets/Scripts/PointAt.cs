using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PointAt : MonoBehaviour
{

    // Update is called once per frame
    void Update()
    {
        Vector3 mousePos = Input.mousePosition;
        mousePos.z = transform.position.z;

        //Vector3 objectPos = Camera.main.WorldToScreenPoint(transform.position);
        //mousePos.x = mousePos.x - objectPos.x;
        //mousePos.y = mousePos.y - objectPos.y;

        //float angle = Mathf.Atan2(mousePos.x, mousePos.y) * Mathf.Rad2Deg;
        //transform.rotation = Quaternion.Euler(new Vector3(0, angle, 0));

        Vector3 mouseWorldPos = Camera.main.ScreenToWorldPoint(mousePos);
        transform.LookAt(mouseWorldPos, Vector3.up);

    }
}
