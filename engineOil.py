#!/usr/bin/env python
# version 2.1

import os
import sys
import logging, logging.handlers
import datetime
import config 


LOG_FILE="/var/log/backup.log"
backup_user="root"

class engineOil:
    def __init__(self):
        self.log()
        config = config.config()
        self.backupDir = config.backupDir
        self.servers = config.servers
        self.databases = config.databases
      
        self.days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        self.weeks = ['weekOne','weekTwo','weekThree','weekFour']
      
        self.setDay()
        
   def makeDailyDirs(self):
      if not os.path.exists (self.backupDir):
         os.makedirs (self.backupDir)
         for day in self.days:
            if not os.path.exists (self.backupDir):
               os.makedirs (self.backupDir + day)
         
   def makeWeeklyDirs(self):
      if not os.path.exists (self.backupDir):
         os.makedirs (self.backupDir)
         for week in self.weeks:
            if not os.path.exists (self.backupDir):
               os.makedirs (self.backupDir + day)
         
   def makePathDirs(self):
      for server, paths in engineOilObj.servers.iteritems():
         for day in self.days:
            for path in paths:
               if not os.path.exists (engineOilObj.backupDir+day+ "/" +server+"/"+path):
                  os.makedirs (engineOilObj.backupDir+day+ "/" +server+"/"+path)
                  
   def log(self):
      """This Function logs to a file and sets up sending an email on error"""
      self.rootLogger = logging.getLogger()
      self.loggingHandler = logging.FileHandler (LOG_FILE)
      self.loggingFormatter = logging.Formatter ('%(asctime)s %(levelname)s %(name)s %(message)s')
      self.loggingHandler.setFormatter (self.loggingFormatter)
      self.rootLogger.setLevel (logging.DEBUG)
      self.rootLogger.addHandler (self.loggingHandler)
      # Logging to email of any errors
      emailHandler = logging.handlers.SMTPHandler ("localhost", "backup@rock", ["root@rock"], "Backup error.")
      emailHandler.setFormatter (self.loggingFormatter)
      emailHandler.setLevel (logging.ERROR)
      self.rootLogger.addHandler (emailHandler)
         
   def runBackup(self):
      for server, paths in self.servers.iteritems():
         for path in paths:
            try:
               os.system("rsync -avz --link-dest=" +self.backupDir+ "linkdest/" +server+path+
                         " --delete -e 'ssh -i /root/engineOil/key.rsa' " +backup_user+ "@"+ server+ ":"+path+
                         " " +self.backupDir+self.folder+ '/' +server+path)
            except Exception, e:
                  logging.error ("Exception occured during backup: %s" % str (e))

   def dumpDatabases(self):
      for server, details in self.databases.iteritems():
         #pp = pprint.PrettyPrinter(indent=4)
         try:
            if 'user' in details:
               user = details['user']
            else:
               user = "root"
            if 'password' in details:
               password = details['password']
            else:
               password = ""
            if 'databases' in details:               
               database = details['databases']
            else:
               database = "--all-databases"
            
            os.system("mysqldump -u" +user+ " -p" +password+ " -h" +server+ " " +database+ " -r " +self.backupDir+self.folder+ '/' +server+ "." +database+ ".sql -R")#"." +self.date+ 
         except Exception, e:
            
            logging.error ("Exception occured during mysqldump: %s" % str (e))
   
   def setType(self, folder):
      if folder != 'daily' or folder != 'weekly':
         print "Failed to set type, folder must be 'daily' or 'weekly'"
         sys.exit()
      self.date = datetime.date.today()
      if folder == 'daily':
         self.setDay()
         self.makeDailyDirs()
      if folder == 'weekly':
         self.setWeek()
         self.makeWeeklyDirs()
      self.date = datetime.date
   
   def setDay(self):
      weekday = self.date.weekday()
      if weekday == 0:
          f = "monday"
      if weekday == 1:
          f = "tuesday"
      if weekday == 2:
          f = "wednesday"
      if weekday == 3:
          f = "thursday"
      if weekday == 4:
          f = "friday"
      if weekday == 5:
          f = "saturday"
      if weekday == 6:
          f = "sunday"
      self.folder = f
      
   
   def setWeek(self):
      day = self.date.day 
      if day <= 7:
         f = 'weekOne'
      if day <= 14 and day  > 7:
         f = 'weekTwo'
      if day <= 21 and day  > 14:
         f = 'weekThree'
      if day  > 21:
         f = 'weekFour'
      self.folder = f
   
if __name__ == "__main__":
   print "This is now only a library class"

