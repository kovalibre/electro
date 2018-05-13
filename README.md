# electro
My first Python programm

Что нового в версии 0.1.1:

 - В теле каждой функции больше не используются глобальные переменные, 
 переменные задаются параметрами функции. (Однако функции все еще зависимы от 
 глобальных констант)
 

Что нового в версии 0.1.0:

 - Разбил всю программу на функции, каждую закомментировал.
 - Ввел возможность журналирования данных, сохранение их в отдельный файл и 
 использовение для текущих рассчетов. Программа теперь полностью выполняет 
 минимум требуемых задач и готова к практическому применению.


Что нового в версии 0.0.4:

 - Ввел функции для проверки вводимых значений (int и float), чтобы вместо 
 остановки программы выводилось сообщение об ошибке.
 - Отдельные функции для вывода рассчетов, появилась возможность выводить 
 данные как по каждой комнате, так и по всем сразу.


Что нового в версии 0.0.3:

 - Избавился от лишних промежуточных переменных (вроде consumption_main = kv[CONSUMPTION]).
 - Назначил более развернутые и, надеюсь, более понятные имена для данных в словарях.
 - Обрезал слишком длинные строки кода при помощи "\".
 - Структурировал и дополнил README.md


Описание программы.

 - Программа предназначена для рассчетов по оплате электроэнергии между 
 жителями коммунальной квартиры.
 - Вводные: мы имеем данные об общем энергопотреблении с основного счетчика 
 и индивидуальные данные по каждой комнате, а также разницу между ними, 
 которая отражает потребление в местах коммунального пользования (душ, коридор,
 кухня). Эта разница делится на всех и оплачивается, исходя из количества 
 проживающих в комнате. 
 - Задачи, которые должна выполнять программа:
   1. Ввод и обработка данных: показания всех счетчиков, количество жильцов, 
   текущий тариф на потребление, неоплаченные долги за предыдущий период.
   2. Вывод результатов рассчетов по каждой комнате: стоимость потребленной 
   собственной и коммунальной электроэнергии, задолженность и итоговая сумма.
   3. Сохранять данные за предыдущие периоды и выводить их по запросу.
   4. Быть масштабируемой до произвольного количества комнат.


Планы по развитию приложения:

 В дальнейших планах портирование программы в веб-интерфейс, создание на ее 
 основе упакованного обособленного решения с более дружелюбным интерфейсом, 
 создание Андроид-приложения с теми же функциями.

