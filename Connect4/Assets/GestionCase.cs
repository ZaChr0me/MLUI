using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class GestionCase : MonoBehaviour
{

    public int state;
    public bool gg;
    // state = 0 -> case vide
    // sate =  1 -> pion J1
    // state = 2 -> pion J2

    // Start is called before the first frame update
    void Start()
    {
        this.state = 0;
        this.gg = false;
    }

    // Update is called once per frame
    void Update()
    {
        if (state == 0)
            gameObject.GetComponent<Image>().color = new Color (157f, 174f, 224f, 0.5f);
        else if (state == 1)
            gameObject.GetComponent<Image>().color = new Color (255f, 255f, 0f, 0.7f);
        else if (state == 2)
            gameObject.GetComponent<Image>().color = new Color (255f, 0f, 0f, 0.7f);

        if (gg==true && state == 1) gameObject.GetComponent<Image>().color = new Color (123f, 255f, 32f, 1f);
        if (gg==true && state == 2) gameObject.GetComponent<Image>().color = new Color (123f, 255f, 32f, 1f);
    }
}
