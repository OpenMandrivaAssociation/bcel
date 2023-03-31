%{?_javapackages_macros:%_javapackages_macros}

Name:           bcel
Version:        6.3.1
Release:        2
Summary:        Byte Code Engineering Library
Group:		Development/Java
License:        ASL 2.0
URL:            http://commons.apache.org/proper/commons-bcel/
# Source for releases:
Source0:        http://archive.apache.org/dist/commons/bcel/source/bcel-%{version}-src.tar.gz
# SVN repository lives at
# svn export http://svn.apache.org/repos/asf/commons/proper/bcel/trunk bcel
BuildArch:      noarch
BuildRequires:	jdk-current
BuildRequires:	javapackages-local

%description
The Byte Code Engineering Library (formerly known as JavaClass) is
intended to give users a convenient possibility to analyze, create, and
manipulate (binary) Java class files (those ending with .class). Classes
are represented by objects which contain all the symbolic information of
the given class: methods, fields and byte code instructions, in
particular.  Such objects can be read from an existing file, be
transformed by a program (e.g. a class loader at run-time) and dumped to
a file again. An even more interesting application is the creation of
classes from scratch at run-time. The Byte Code Engineering Library
(BCEL) may be also useful if you want to learn about the Java Virtual
Machine (JVM) and the format of Java .class files.  BCEL is already
being used successfully in several projects such as compilers,
optimizers, obsfuscators and analysis tools, the most popular probably
being the Xalan XSLT processor at Apache.

%package javadoc
Summary:        API documentation for %{name}
Obsoletes:      %{name}-manual < %{version}-%{release}

%description javadoc
This package provides %{summary}.

%prep
%autosetup -p1 -n %{name}-%{version}-src

%build
. %{_sysconfdir}/profile.d/90java.sh
export PATH=$JAVA_HOME/bin:$PATH
export LANG=en_US.utf-8

buildjar() {
	MODULE="$1"
	shift
	echo "module $MODULE {" >module-info.java
	find . -name "*.java" |xargs grep ^package |sed -e 's,^.*package ,,;s,\;.*,,' |sort |uniq |while read e; do
		echo "  exports $e;" >>module-info.java
	done
	for i in "$@"; do
		echo "	requires $i;" >>module-info.java
	done
	echo '}' >>module-info.java
	find . -name "*.java" |xargs javac
	find . -name "*.class" -o -name "*.properties" |xargs jar cf $MODULE-%{version}.jar
	jar i $MODULE-%{version}.jar
	javadoc -d docs -sourcepath . $MODULE
}
cd src/main/java
buildjar org.apache.bcel java.desktop

%install
mkdir -p %{buildroot}%{_javadir}/modules %{buildroot}%{_mavenpomdir} %{buildroot}%{_javadocdir}
cp src/main/java/org.apache.bcel-%{version}.jar %{buildroot}%{_javadir}/modules
ln -s modules/org.apache.bcel-%{version}.jar %{buildroot}%{_javadir}/
ln -s modules/org.apache.bcel-%{version}.jar %{buildroot}%{_javadir}/org.apache.bcel.jar
mv pom.xml org.apache.bcel-%{version}.pom
cp *.pom %{buildroot}%{_mavenpomdir}/
%add_maven_depmap org.apache.bcel-%{version}.pom org.apache.bcel-%{version}.jar
cp -a src/main/java/docs %{buildroot}%{_javadocdir}/%{name}


%files -f .mfiles
%{_datadir}/java/modules/*.jar
%{_datadir}/java/*.jar

%files javadoc
%{_javadocdir}/%{name}
