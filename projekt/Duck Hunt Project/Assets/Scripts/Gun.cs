using System.Collections;
using System.Collections.Generic;
using System;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class Gun : MonoBehaviour
{

    public ParticleSystem muzzleFlash;
    public ParticleSystem smoke;
    public ParticleSystem feathers;
    public TextMeshProUGUI score;
    public AudioSource quack;
    private AudioSource audio;

    void Start()
    {
        audio = GetComponent<AudioSource>();
    }

    // Update is called once per frame
    void Update()
    {
        Vector3 mousePos = Input.mousePosition;
        mousePos.z = transform.position.z;

        Vector3 mouseWorldPos = Camera.main.ScreenToWorldPoint(mousePos);
        transform.LookAt(mouseWorldPos, Vector3.up);
        transform.eulerAngles = new Vector3(-transform.eulerAngles.x - 15, transform.eulerAngles.y - 180, transform.eulerAngles.z);

        if(Input.GetButtonDown("Fire1"))
        {
            audio.Play();
            muzzleFlash.Play();
            Ray ray = Camera.main.ScreenPointToRay(mousePos);

            if(Physics.Raycast(ray, out RaycastHit hitData))
            {
            
                Destroy(hitData.transform.gameObject);

                
                GameObject poof = Instantiate(smoke.gameObject, hitData.transform.position, Quaternion.identity);
                GameObject feath = Instantiate(feathers.gameObject, hitData.transform.position, Quaternion.identity);
                poof.transform.position += new Vector3(0, 1.5f, 0);
                feath.transform.position += new Vector3(0, 1.5f, 0);
                Destroy(poof, 3.0f);
                Destroy(feath, 3.0f);
                quack.Play();

                int currScore = Convert.ToInt32(score.text);
                currScore += 10;
                score.text = currScore.ToString();
            }
        }
    }
}
