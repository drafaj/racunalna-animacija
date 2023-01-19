using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Mallard : MonoBehaviour
{
    public float life = 4;

    void Awake()
    {
        Destroy(gameObject, life);
    }
}
