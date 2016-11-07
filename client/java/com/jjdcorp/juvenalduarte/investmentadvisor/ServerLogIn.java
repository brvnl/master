package com.jjdcorp.juvenalduarte.investmentadvisor;

import java.io.*;
import java.net.*;

/**
 * Created by juvenalduarte on 16/10/16.
 */

public class ServerLogIn {
    public String user;
    public String password;
    public String host;
    public int port;

    ServerLogIn(String aUser, String aPassword) {
        this.user = aUser;
        this.password = aPassword;
        this.host = ServerDetails.getLoginServerHostIP();
        this.port = ServerDetails.getLoginServerHostPort();
    }

    public int Authenticate() {
        int status = 1;

        try{
            InetAddress serverAddr = InetAddress.getByName(host);
            Socket soc = new Socket(serverAddr,port);
            DataOutputStream dout=new DataOutputStream(soc.getOutputStream());
            String authString = "@authenticate;user:" + user + ";password:" + password + ";";
            dout.flush();
            dout.writeUTF(authString);

            DataInputStream input = new DataInputStream(soc.getInputStream());
            BufferedReader br = new BufferedReader(new InputStreamReader(soc.getInputStream()));

            String incoming = "";
            //while ((incoming = input.readUTF()) != null) {
            while ((incoming = br.readLine()) != null) {
                System.out.println("DEBUG* \n\n");
                System.out.println(incoming);

                if (incoming.equals("Succeed")) {
                    status = 0;
                    break;
                } else if (incoming.equals("Wrong Pass")) {
                    status = 3;
                    break;
                } else if (incoming.equals("Failed")) {
                    status = 1;
                    break;
                } else {
                    status = 1;
                    break;
                }
            }

            dout.flush();
            dout.close();
            //soc.close();
        }catch(Exception e){
            e.printStackTrace();
            status = 2;
        }

        return status;
    }
}
