using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class GestionGrille : MonoBehaviour
{


    private GameObject[,] ensembleCases;
    public int ActivePlayer;

    // Start is called before the first frame update
    void Start()
    {
        ActivePlayer = 1;
        ensembleCases = new GameObject[7,5];
        int acc = 0;
        for (int i=0; i<5; i++)
        {
            for (int j=0; j<7; j++)
            {
                ensembleCases[j,i] = this.gameObject.transform.GetChild(acc).gameObject;
                //this.gameObject.transform.GetChild(acc).gameObject.GetComponent<GestionCase>().state = 1;
                acc++;
            }
        }

    }

    // Update is called once per frame
    void Update()
    {
        //randomCell.GetComponent<GestionCase>().state = 1;
        //ensembleCases[2,3].GetComponent<GestionCase>().state = 1;
        
        if (Input.GetKeyDown(KeyCode.Alpha1))
        {
            Action(0);
        }
        if (Input.GetKeyDown(KeyCode.Alpha2))
        {
            Action(1);
        }
        if (Input.GetKeyDown(KeyCode.Alpha3))
        {
            Action(2);
        }
        if (Input.GetKeyDown(KeyCode.Alpha4))
        {
            Action(3);
        }
        if (Input.GetKeyDown(KeyCode.Alpha5))
        {
            Action(4);
        }
        if (Input.GetKeyDown(KeyCode.Alpha6))
        {
            Action(5);
        }
        if (Input.GetKeyDown(KeyCode.Alpha7))
        {
            Action(6);
        }
        

        int a = cvAll();
    }

    public void Action (int colone)
    {
        // ajouter ceci ->  check si colone <0-6>

        for (int i=4; i>=0; i--)
        {
            if (ensembleCases[colone,i].GetComponent<GestionCase>().state == 0) 
            {
                ensembleCases[colone,i].GetComponent<GestionCase>().state = ActivePlayer;
                if (ActivePlayer==1) ActivePlayer = 2;
                else if (ActivePlayer==2) ActivePlayer = 1;
                return;
            }
        }
    }

    private int cvHorisontal (int ligne, int colone)
    {
        if (ensembleCases[colone,ligne].GetComponent<GestionCase>().state 
        == ensembleCases[colone+1,ligne].GetComponent<GestionCase>().state 
        && ensembleCases[colone,ligne].GetComponent<GestionCase>().state
        == ensembleCases[colone+2,ligne].GetComponent<GestionCase>().state 
        && ensembleCases[colone,ligne].GetComponent<GestionCase>().state
        == ensembleCases[colone+3,ligne].GetComponent<GestionCase>().state
        && ensembleCases[colone,ligne].GetComponent<GestionCase>().state != 0 )
        {
            ensembleCases[colone,ligne].GetComponent<GestionCase>().gg = true;
             ensembleCases[colone+1,ligne].GetComponent<GestionCase>().gg = true;
             ensembleCases[colone+2,ligne].GetComponent<GestionCase>().gg = true;
             ensembleCases[colone+3,ligne].GetComponent<GestionCase>().gg = true;
            return ensembleCases[colone,ligne].GetComponent<GestionCase>().state;
        }
        return 0;
    }

    private int cvVertical (int ligne, int colone)
    {
        if (ensembleCases[colone,ligne].GetComponent<GestionCase>().state 
         == ensembleCases[colone,ligne+1].GetComponent<GestionCase>().state
         && ensembleCases[colone,ligne].GetComponent<GestionCase>().state 
         == ensembleCases[colone,ligne+2].GetComponent<GestionCase>().state
         && ensembleCases[colone,ligne].GetComponent<GestionCase>().state 
         == ensembleCases[colone,ligne+3].GetComponent<GestionCase>().state
         && ensembleCases[colone,ligne].GetComponent<GestionCase>().state != 0 )
        {
            ensembleCases[colone,ligne].GetComponent<GestionCase>().gg = true;
             ensembleCases[colone,ligne+1].GetComponent<GestionCase>().gg = true;
             ensembleCases[colone,ligne+2].GetComponent<GestionCase>().gg = true;
             ensembleCases[colone,ligne+3].GetComponent<GestionCase>().gg = true;
            return ensembleCases[colone,ligne].GetComponent<GestionCase>().state;
        }
        return 0;
    }

    private int cvDiag1 (int ligne, int colone)
    {
        if (ensembleCases[colone,ligne].GetComponent<GestionCase>().state 
         == ensembleCases[colone+1,ligne+1].GetComponent<GestionCase>().state 
         && ensembleCases[colone,ligne].GetComponent<GestionCase>().state
         == ensembleCases[colone+2,ligne+2].GetComponent<GestionCase>().state 
         && ensembleCases[colone,ligne].GetComponent<GestionCase>().state
         == ensembleCases[colone+3,ligne+3].GetComponent<GestionCase>().state
         && ensembleCases[colone,ligne].GetComponent<GestionCase>().state != 0 )
        {
            ensembleCases[colone,ligne].GetComponent<GestionCase>().gg = true;
             ensembleCases[colone+1,ligne+1].GetComponent<GestionCase>().gg = true;
             ensembleCases[colone+2,ligne+2].GetComponent<GestionCase>().gg = true;
             ensembleCases[colone+3,ligne+3].GetComponent<GestionCase>().gg = true;
            return ensembleCases[colone,ligne].GetComponent<GestionCase>().state;
        }
        return 0;
    }
    private int cvDiag2 (int ligne, int colone)
    {
        if (ensembleCases[colone,ligne+3].GetComponent<GestionCase>().state 
         == ensembleCases[colone+1,ligne+2].GetComponent<GestionCase>().state 
         && ensembleCases[colone,ligne+3].GetComponent<GestionCase>().state
         == ensembleCases[colone+2,ligne+1].GetComponent<GestionCase>().state 
         && ensembleCases[colone,ligne+3].GetComponent<GestionCase>().state
         == ensembleCases[colone+3,ligne].GetComponent<GestionCase>().state 
         && ensembleCases[colone,ligne+3].GetComponent<GestionCase>().state != 0)
        {
            ensembleCases[colone,ligne+3].GetComponent<GestionCase>().gg = true;
             ensembleCases[colone+1,ligne+2].GetComponent<GestionCase>().gg = true;
             ensembleCases[colone+2,ligne+1].GetComponent<GestionCase>().gg = true;
             ensembleCases[colone+3,ligne].GetComponent<GestionCase>().gg = true;
            return ensembleCases[colone,ligne+3].GetComponent<GestionCase>().state;
        }
        return 0;
    }

    private int cvAll ()
    {
        int tmp = 0;
        for (int i=0; i<4; i++)
        {
            for (int j=0; j<2; j++)
            {
                tmp = cvDiag1(j, i);
                if (tmp != 0) return tmp;

                tmp = cvDiag2(j, i);
                if (tmp != 0) return tmp;
            }
        }

        for (int i=0; i<4; i++)
        {
            for (int j=0; j<5; j++)
            {
                tmp = cvHorisontal(j, i);
                if (tmp != 0) return tmp;

            }
        }
        
        for (int i=0; i<7; i++)
        {
            for (int j=0; j<2; j++)
            {
                tmp = cvVertical(j, i);
                if (tmp != 0) return tmp;

            }
        }


        return tmp;
    }
}
