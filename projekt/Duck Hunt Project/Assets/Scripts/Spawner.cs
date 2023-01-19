using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Spawner : MonoBehaviour
{
    public GameObject mallardprefab;
    public float startTime = 1;
    public float speed = 5;
    public Vector3 mallardrot;

    private float targetTime;

    // Start is called before the first frame update
    void Start()
    {
        //InvokeRepeating("SpawnObject", startTime, spawnInterval);
        targetTime = startTime;
    }

    void Update()
    {
        targetTime -= Time.deltaTime;
        if (targetTime <= 0)
        {
            SpawnObject();
            targetTime = Random.Range(4, 7);
        }
    }

    public void SpawnObject()
    {
        //Quaternion rotation = Quaternion.LookRotation(mallardrot, Vector3.up);
        
        //var mallard = Instantiate(mallardprefab, transform.position, rotation);

        var mallard = Instantiate(mallardprefab, transform);
        mallard.transform.LookAt(transform, Vector3.up);
        mallard.transform.eulerAngles = new Vector3(mallard.transform.eulerAngles.x, -mallard.transform.eulerAngles.y - 90, mallard.transform.eulerAngles.z);
        mallard.GetComponent<Rigidbody>().velocity = transform.forward * speed;

    }
}
