.source Main.java
.class public Main
.super java/lang/Object

.method public static main([Ljava/lang/String;)V
Label0:
.var 0 is args Ljava/lang/Object; from Label0 to Label1
	ldc "--- Literal Values ---"
	invokestatic baolang/BaoLangFunctions/print(Ljava/lang/Object;)Ljava/lang/Object;
	iconst_1
	invokestatic java/lang/Boolean/valueOf(Z)Ljava/lang/Boolean;
	invokestatic baolang/BaoLangFunctions/print(Ljava/lang/Object;)Ljava/lang/Object;
	bipush 42
	invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
	invokestatic baolang/BaoLangFunctions/print(Ljava/lang/Object;)Ljava/lang/Object;
.var 1 is a Ljava/lang/Object; from Label0 to Label1
	bipush 10
	invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
	astore_1
.var 2 is b Ljava/lang/Object; from Label0 to Label1
	bipush 20
	invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
	astore_2
.var 3 is c Ljava/lang/Object; from Label0 to Label1
	aload_1
	aload_2
	invokestatic baolang/BaoLangOperators/add(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
	astore_3
	ldc "--- Basic Operations ---"
	invokestatic baolang/BaoLangFunctions/print(Ljava/lang/Object;)Ljava/lang/Object;
	aload_3
	invokestatic baolang/BaoLangFunctions/print(Ljava/lang/Object;)Ljava/lang/Object;
	ldc "--- Functions and Lambdas ---"
	invokestatic baolang/BaoLangFunctions/print(Ljava/lang/Object;)Ljava/lang/Object;
.var 4 is add Ljava/lang/Object; from Label0 to Label1
	new Lambda0
	dup
	invokespecial Lambda0/<init>()V
	astore 4
	aload 4
	new java/util/ArrayList
	dup
	invokespecial java/util/ArrayList/<init>()V
	dup
	iconst_5
	invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
	invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
	pop
	dup
	bipush 7
	invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
	invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
	pop
	invokeinterface baolang/LambdaInterface/call(Ljava/util/ArrayList;)Ljava/lang/Object; 2
	invokestatic baolang/BaoLangFunctions/print(Ljava/lang/Object;)Ljava/lang/Object;
.var 5 is succ Ljava/lang/Object; from Label0 to Label1
	new Lambda1
	dup
	invokespecial Lambda1/<init>()V
	astore 5
.var 6 is g Ljava/lang/Object; from Label0 to Label1
	new Lambda2
	dup
	invokespecial Lambda2/<init>()V
	astore 6
	ldc "--- High level function ---"
	invokestatic baolang/BaoLangFunctions/print(Ljava/lang/Object;)Ljava/lang/Object;
	aload 6
	new java/util/ArrayList
	dup
	invokespecial java/util/ArrayList/<init>()V
	dup
	aload 5
	invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
	pop
	dup
	iconst_5
	invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
	invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
	pop
	invokeinterface baolang/LambdaInterface/call(Ljava/util/ArrayList;)Ljava/lang/Object; 2
	invokestatic baolang/BaoLangFunctions/print(Ljava/lang/Object;)Ljava/lang/Object;
.var 7 is func Ljava/lang/Object; from Label0 to Label1
	new Lambda3
	dup
	invokespecial Lambda3/<init>()V
	astore 7
	ldc "--- Currying ---"
	invokestatic baolang/BaoLangFunctions/print(Ljava/lang/Object;)Ljava/lang/Object;
	aload 7
	new java/util/ArrayList
	dup
	invokespecial java/util/ArrayList/<init>()V
	dup
	iconst_5
	invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
	invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
	pop
	invokeinterface baolang/LambdaInterface/call(Ljava/util/ArrayList;)Ljava/lang/Object; 2
	new java/util/ArrayList
	dup
	invokespecial java/util/ArrayList/<init>()V
	dup
	bipush 6
	invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
	invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
	pop
	invokeinterface baolang/LambdaInterface/call(Ljava/util/ArrayList;)Ljava/lang/Object; 2
	new java/util/ArrayList
	dup
	invokespecial java/util/ArrayList/<init>()V
	dup
	bipush 7
	invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
	invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
	pop
	invokeinterface baolang/LambdaInterface/call(Ljava/util/ArrayList;)Ljava/lang/Object; 2
	invokestatic baolang/BaoLangFunctions/print(Ljava/lang/Object;)Ljava/lang/Object;
	return
Label1:
.limit stack 64
.limit locals 8
.end method
