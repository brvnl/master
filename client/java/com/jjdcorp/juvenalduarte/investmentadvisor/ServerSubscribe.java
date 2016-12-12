package com.jjdcorp.juvenalduarte.investmentadvisor;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.net.InetAddress;
import java.net.Socket;

/**
 * Created by juvenalduarte on 23/10/16.
 */

public class ServerSubscribe extends ServerLogIn {
    private String keys;
    private String nkeys;

    ServerSubscribe(String aUser, String aPassword, String aKeywords) {
        super(aUser, aPassword);
        keys = aKeywords;
        nkeys = "";
    }

    ServerSubscribe(String aUser, String aPassword, String aKeywords, String aNKeywords) {
        super(aUser, aPassword);
        keys = aKeywords;
        nkeys = aNKeywords;
    }

    public int Register() {
        int status = 2;

        try{
            InetAddress serverAddr = InetAddress.getByName(host);
            Socket soc = new Socket(serverAddr,port);
            DataOutputStream dout=new DataOutputStream(soc.getOutputStream());
            String registerString = "@register;user:" + user + ";password:" + password + ";" + keys + ";" + nkeys;
            dout.writeUTF(registerString);

            DataInputStream input = new DataInputStream(soc.getInputStream());
            BufferedReader br = new BufferedReader(new InputStreamReader(soc.getInputStream()));

            String incoming = "";
            //while ((incoming = input.readUTF()) != null) {
            while ((incoming = br.readLine()) != null) {
                System.out.println(incoming);

                if (incoming.equals("Succeed")) {
                    status = 0;
                    break;
                } else if (incoming.equals("Already exists")) {
                    status = 1;
                    break;
                } else {
                    status = 2;
                    break;
                }
            }

            dout.flush();
            dout.close();
            soc.close();
        }catch(Exception e){
            e.printStackTrace();
            status = 2;
        }

        return status;
    }

    public int Update() {
        int status = 2;

        try{
            InetAddress serverAddr = InetAddress.getByName(host);
            Socket soc = new Socket(serverAddr,port);
            DataOutputStream dout=new DataOutputStream(soc.getOutputStream());
            String registerString = "@updatekeys;user:" + user + ";password:" + password + ";" + keys + ";" + nkeys;
            dout.writeUTF(registerString);

            DataInputStream input = new DataInputStream(soc.getInputStream());
            BufferedReader br = new BufferedReader(new InputStreamReader(soc.getInputStream()));

            String incoming = "";
            while ((incoming = br.readLine()) != null) {
                System.out.println(incoming);

                if (incoming.equals("Succeed")) {
                    status = 0;
                    break;
                } else {
                    status = 2;
                    break;
                }
            }

            dout.flush();
            dout.close();
            soc.close();
        }catch(Exception e){
            e.printStackTrace();
            status = 2;
        }

        return status;
    }
}
