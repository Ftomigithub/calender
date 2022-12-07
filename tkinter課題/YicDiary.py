import tkinter as tk
import tkinter.ttk as ttk
import datetime as da
import calendar as ca
import pymysql.cursors

WEEK = ['日', '月', '火', '水', '木', '金', '土']
WEEK_COLOUR = ['red', 'black', 'black', 'black','black', 'black', 'blue']
actions = ('学校','試験', '課題', '行事', '就活', 'アルバイト','旅行')


class Login():
    '''ログインを制御するクラス'''

    def __init__(self, master, main):
        '''コンストラクタ
            master:ログイン画面を配置するウィジェット
            body:アプリ本体のクラスのインスタンス
        '''

        self.master = master

        # アプリ本体のクラスのインスタンスをセット
        self.main = main

        # ログイン関連のウィジェットを管理するリスト
        self.widgets = []

        # ログイン画面のウィジェット作成
        self.create_widgets()

    def create_widgets(self):
        '''ウィジェットを作成・配置する'''

        # ユーザー名入力用のウィジェット
        self.name_label = tk.Label(
            self.master,
            text="ユーザー名"
        )
        self.name_label.grid(
            row=0,
            column=0
        )
        self.widgets.append(self.name_label)

        self.name_entry = tk.Entry(self.master)
        self.name_entry.grid(
            row=0,
            column=1
        )
        self.widgets.append(self.name_entry)

        # パスワード入力用のウィジェット
        self.pass_label = tk.Label(
            self.master,
            text="パスワード"
        )
        self.pass_label.grid(
            row=1,
            column=0
        )
        self.widgets.append(self.pass_label)

        self.pass_entry = tk.Entry(
            self.master,
            show="*"
        )
        self.pass_entry.grid(
            row=1,
            column=1
        )
        self.widgets.append(self.pass_entry)

        # ログインボタン
        self.login_button = tk.Button(
            self.master,
            text="ログイン",
            command=self.login
        )
        self.login_button.grid(
            row=2,
            column=0,
            columnspan=2,
        )
        self.widgets.append(self.login_button)

        # ウィジェット全てを中央寄せ
        self.master.grid_anchor(tk.CENTER)

        # 登録ボタン (今回は使わない)
    '''
        self.register_button = tk.Button(
            self.master,
            text="登録",
            command=self.register
        )
        self.register_button.grid(
            row=3,
            column=0,
            columnspan=2,
        )
        self.widgets.append(self.register_button)

    '''

    def login(self):
        '''ログインを実行する'''

        # 入力された情報をEntryウィジェットから取得
        username = self.name_entry.get()
        password = self.pass_entry.get()

        # 登録済みのユーザー名とパスワードを取得
        connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password= '',
                                 db= 'mytest',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

        try:
            # トランザクション関数
            connection.begin()

            with connection.cursor() as cursor:
                cursor = connection.cursor()

        
            # 登録されているものと一致するかを確認
            sql = "select * from users where exists (select * from users where user = '{}' and password = '{}')".format(username, password)

            # SQLの実行
            cursor.execute(sql)
            resurt  = cursor.fetchall()
            if len(resurt) != 0:
                self.login_name = username

                self.success()

            # 入力された情報が登録されていない場合
            else:
                self.fail()
        
            connection.commit() 
        except Exception as e:
            print('error:', e)
            connection.rollback()
        finally:
            connection.close()  
    '''
    def register(self):
ユーザー名とパスワードを登録する

        # 入力された情報をEntryウィジェットから取得
        username = self.name_entry.get()
        password = self.pass_entry.get()

    '''

    def fail(self):
        '''ログイン失敗時の処理を行う'''

        # 表示中のウィジェットを一旦削除
        for widget in self.widgets:
            widget.destroy()

        # "ログインに失敗しました"メッセージを表示
        self.message = tk.Label(
            self.master,
            text="ログインに失敗しました",
            font=("",40)
        )
        self.message.place(
            x=self.master.winfo_width() // 2,
            y=self.master.winfo_height() // 2,
            anchor=tk.CENTER
        )

        # 少しディレイを入れてredisplayを実行
        self.master.after(1000, self.redisplay)

    def redisplay(self):
        '''ログイン画面を再表示する'''

        # "ログインできませんでした"メッセージを削除
        self.message.destroy()

        # ウィジェットを再度作成・配置
        self.create_widgets()

    def success(self):
        '''ログイン成功時の処理を実行する'''

        # 表示中のウィジェットを一旦削除
        for widget in self.widgets:
            widget.destroy()

        # "ログインに成功しました"メッセージを表示
        self.message = tk.Label(
            self.master,
            text="ログインに成功しました",
            font=("",40)
        )
        self.message.place(
            x=self.master.winfo_width() // 2,
            y=self.master.winfo_height() // 2,
            anchor=tk.CENTER
        )

        
        self.master.after(1000, self.main_start)
        self.create_widgets.destroy()

    def main_start(self):
        '''アプリ本体を起動する'''

        # "ログインに成功しました"メッセージを削除
        self.message.destroy()
                # 表示中のウィジェットを一旦削除
        for widget in self.widgets:
            widget.destroy()


        # アプリ本体を起動
        root = tk.Tk()
        self.main.start(root, self.login_name)
        

class YicDiary:
  def __init__(self, master):
    '''
            コンストラクタ
            master:ログイン画面を配置するウィジェット
    '''

    self.master = master
  def start(self, root, master):

    self.users = master

    root.title('予定管理アプリ               ' + self.users + "でログイン中")
    root.geometry('520x280')
    root.resizable(0, 0)
    root.grid_columnconfigure((0, 1), weight=1)
    self.sub_win = None

    self.year  = da.date.today().year
    self.mon = da.date.today().month
    self.today = da.date.today().day

    self.title = None
    # 左側のカレンダー部分
    leftFrame = tk.Frame(root)
    leftFrame.grid(row=0, column=0)
    self.leftBuild(leftFrame)

    # 右側の予定管理部分
    rightFrame = tk.Frame(root)
    rightFrame.grid(row=0, column=1)
    self.rightBuild(rightFrame)



  #-----------------------------------------------------------------
  # アプリの左側の領域を作成する
  #
  # leftFrame: 左側のフレーム
  def leftBuild(self, leftFrame):
    self.viewLabel = tk.Label(leftFrame, font=('', 10))
    beforButton = tk.Button(leftFrame, text='＜', font=('', 10), command=lambda:self.disp(-1))
    nextButton = tk.Button(leftFrame, text='＞', font=('', 10), command=lambda:self.disp(1))

    self.viewLabel.grid(row=0, column=1, pady=10, padx=10)
    beforButton.grid(row=0, column=0, pady=10, padx=10)
    nextButton.grid(row=0, column=2, pady=10, padx=10)

    self.calendar = tk.Frame(leftFrame)
    self.calendar.grid(row=1, column=0, columnspan=3)
    self.disp(0)


  #-----------------------------------------------------------------
  # アプリの右側の領域を作成する
  #
  # rightFrame: 右側のフレーム
  def rightBuild(self, rightFrame):
    r1_frame = tk.Frame(rightFrame)
    r1_frame.grid(row=0, column=0, pady=10)
    r2_frame = tk.Frame(rightFrame)
    r2_frame.grid(row=5, column=0, pady=10)


    temp = '{}年{}月{}日の予定'.format(self.year, self.mon, self.today)
    self.title = tk.Label(r1_frame, text=temp, font=('', 12))
    self.title.grid(row=0, column=0, padx=20)

    self.title2 = tk.Label(r2_frame, text=temp, font=('', 10))
    self.title2.grid(row=0, column=0, padx=10)

    button = tk.Button(rightFrame, text='追加', command=lambda:self.add())
    button.grid(row=0, column=1)
    
    self.schedule()


  #-----------------------------------------------------------------
  # アプリの右側の領域に予定を表示する
  #
  def schedule(self):
    self.title2['text'] = '{}'.format(self.dbmemo())

    
    # ウィジットを廃棄
    '''
    for widget in self.r2_frame.winfo_children():
      widget.destroy()
    '''


    # データベースに予定の問い合わせを行う
  def dbmemo(self):

    memo = ''

    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password= '',
                                 db= 'mytest',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        # トランザクション関数
        connection.begin()

        with connection.cursor() as cursor:
            cursor = connection.cursor()

            sql = "select user, memo from schedule inner join users on schedule.userID = users.userID where days = '{}-{}-{}'".format(self.year, self.mon, self.today)

            print(sql)


            # SQLの実行
            cursor.execute(sql)



            userlist = cursor.fetchall()

            sql = "select memo from schedule where days = '{}-{}-{}'".format(self.year, self.mon, self.today)

            print(sql)


            # SQLの実行
            cursor.execute(sql)

            memos = cursor.fetchall()

            print(userlist)

            print(memos)


            for i, text in enumerate(userlist):
                print(text["user"])
                print(text["memo"])
                memo = memo + '\n' + text["user"]
                memo = memo + ':' + text["memo"]





        connection.commit()

    except Exception as e:
        print('error:', e)
        connection.rollback()
    finally:
        connection.close()  

    return memo


  #-----------------------------------------------------------------
  # カレンダーを表示する
  #
  # argv: -1 = 前月
  #        0 = 今月（起動時のみ）
  #        1 = 次月
  def disp(self, argv):
    self.mon = self.mon + argv
    if self.mon < 1:
      self.mon, self.year = 12, self.year - 1
    elif self.mon > 12:
      self.mon, self.year = 1, self.year + 1

    self.viewLabel['text'] = '{}年{}月'.format(self.year, self.mon)

    cal = ca.Calendar(firstweekday=6)
    cal = cal.monthdayscalendar(self.year, self.mon)

    # ウィジットを廃棄
    for widget in self.calendar.winfo_children():
      widget.destroy()

    # 見出し行
    r = 0
    for i, x in enumerate(WEEK):
      label_day = tk.Label(self.calendar, text=x, font=('', 10), width=3, fg=WEEK_COLOUR[i])
      label_day.grid(row=r, column=i, pady=1)

    # カレンダー本体
    r = 1
    for week in cal:
      for i, day in enumerate(week):
        if day == 0: day = ' ' 
        label_day = tk.Label(self.calendar, text=day, font=('', 10), fg=WEEK_COLOUR[i], borderwidth=1)
        if (da.date.today().year, da.date.today().month, da.date.today().day) == (self.year, self.mon, day):
          label_day['relief'] = 'solid'
        label_day.bind('<Button-1>', self.click)
        label_day.grid(row=r, column=i, padx=2, pady=1)
      r = r + 1

    # 画面右側の表示を変更
    if self.title is not None:
      self.today = 1
      self.title['text'] = '{}年{}月{}日の予定'.format(self.year, self.mon, self.today)


  #-----------------------------------------------------------------
  # 予定を追加したときに呼び出されるメソッド
  #
  def add(self):
    if self.sub_win == None or not self.sub_win.winfo_exists():
      self.sub_win = tk.Toplevel()
      self.sub_win.geometry("300x300")
      self.sub_win.resizable(0, 0)

      # ラベル
      sb1_frame = tk.Frame(self.sub_win)
      sb1_frame.grid(row=0, column=0)
      temp = '{}年{}月{}日　追加する予定'.format(self.year, self.mon, self.today)
      title = tk.Label(sb1_frame, text=temp, font=('', 12))
      title.grid(row=0, column=0)

      # 予定種別（コンボボックス）
      sb2_frame = tk.Frame(self.sub_win)
      sb2_frame.grid(row=1, column=0)
      label_1 = tk.Label(sb2_frame, text='種別 : 　', font=('', 10))
      label_1.grid(row=0, column=0, sticky=tk.W)
      self.combo = ttk.Combobox(sb2_frame, state='readonly', values=actions)
      self.combo.current(0)
      self.combo.grid(row=0, column=1)

      # テキストエリア（垂直スクロール付）
      sb3_frame = tk.Frame(self.sub_win)
      sb3_frame.grid(row=2, column=0)
      self.text = tk.Text(sb3_frame, width=40, height=15)
      self.text.grid(row=0, column=0)
      scroll_v = tk.Scrollbar(sb3_frame, orient=tk.VERTICAL, command=self.text.yview)
      scroll_v.grid(row=0, column=1, sticky=tk.N+tk.S)
      self.text["yscrollcommand"] = scroll_v.set

      # 保存ボタン
      sb4_frame = tk.Frame(self.sub_win)
      sb4_frame.grid(row=3, column=0, sticky=tk.NE)
      button = tk.Button(sb4_frame, text='保存', command=lambda:self.done())
      button.pack(padx=10, pady=10)
    elif self.sub_win != None and self.sub_win.winfo_exists():
      self.sub_win.lift()



  #-----------------------------------------------------------------
  # 予定追加ウィンドウで「保存」を押したときに呼び出されるメソッド
  #
  def done(self):
    
    # 日付
    days = '{}-{}-{}'.format(self.year, self.mon, self.today)
    print(days)

    # 種別
    kinds = self.combo.get()
    print(kinds)

    # memo
    memo = self.text.get("1.0", "end")
    memo = memo.replace('\n',' ')
    print(memo)

    # データベースに新規予定を挿入する

    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password= '',
                                 db= 'mytest',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        # トランザクション関数
        connection.begin()

        with connection.cursor() as cursor:
            cursor = connection.cursor()


            sql = "select kindsID from kind where kinds = '{}'".format(kinds)

            print(sql)



            # SQLの実行
            cursor.execute(sql)

            rows = cursor.fetchall()
            for i, row in enumerate(rows):
                print(row["kindsID"])

            kindsID = row["kindsID"]

            sql = "select userID from users where user = '{}'".format(self.users)

            print(sql)



            # SQLの実行
            cursor.execute(sql)

            rows = cursor.fetchall()
            for i, row in enumerate(rows):
                print(row["userID"])

            userID = row["userID"]

            

            sql = "insert into schedule (days, kindsID, userID, memo) values('{}', {}, {}, '{}')".format(days, kindsID, userID, memo)

            print(sql)

            # SQLの実行
            cursor.execute(sql)

            results = cursor.fetchall()
            for i, row in enumerate(results):
                print(i, row)
            
            sql = "select * from schedule"

            print(sql)

            # SQLの実行
            cursor.execute(sql)

            results = cursor.fetchall()
            for i, row in enumerate(results):
                print(i, row)
            
        connection.commit()

    except Exception as e:
        print('error:', e)
        connection.rollback()
    finally:
        connection.close()

    self.schedule()

    self.sub_win.destroy()

  #-----------------------------------------------------------------
  # 日付をクリックした際に呼びだされるメソッド（コールバック関数）
  #
  # event: 左クリックイベント <Button-1>
  def click(self, event):
    day = event.widget['text']


    if day != ' ':
        self.title['text'] = '{}年{}月{}日の予定'.format(self.year, self.mon, day)
        self.today = day

    self.schedule()




def Main():
  app = tk.Tk()

# メインウィンドウのサイズ設定
  app.geometry("600x400")

# アプリ本体のインスタンス生成
  main = YicDiary(app)

# ログイン管理クラスのインスタンス生成
  login = Login(app, main)

  Login(app, main)
  app.mainloop()

if __name__ == '__main__':
  Main()
