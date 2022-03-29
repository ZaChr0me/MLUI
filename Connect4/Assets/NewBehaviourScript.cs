using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NewBehaviourScript : MonoBehaviour
{
    public bool test;
    public GameObject nouveauTest;

    // Start is called before the first frame update
    void Start()
    {
        this.test = false;
    }

    // Update is called once per frame
    void Update()
    {
        this.test = true;
    }
}
