from rich.console import Console
from rich.table import Table

def pretty_print_risk_evaluation(공종, 공정, 작업명, 위험성평가표, 기타):
    console = Console()

    # 헤더 출력
    console.print(f"\n[bold cyan]공종:[/bold cyan] {공종}  |  [bold cyan]공정:[/bold cyan] {공정}")
    console.print(f"[bold green]작업명:[/bold green] {작업명}\n")

    # 테이블 생성
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("번호", justify="center")
    table.add_column("설비", justify="center")
    table.add_column("물질", justify="center")
    table.add_column("유해·위험 요인_분류", justify="left")
    table.add_column("유해·위험 요인", justify="left")
    table.add_column("관련 근거", justify="left")
    table.add_column("가능성", justify="center")
    table.add_column("중대성", justify="center")
    table.add_column("위험성", justify="center")
    table.add_column("감소 대책", justify="left", max_width=40, overflow="fold")

    if isinstance(위험성평가표, str):
        console.print("[bold red]⚠️ 평가표가 문자열로 들어왔습니다.[/bold red]")
        return

    elif isinstance(위험성평가표, list):
        for item in 위험성평가표:
            # 감소대책 포맷 처리
            if isinstance(item.감소대책, list):
                감소대책_str = " • ".join(d.strip() for d in item.감소대책 if d.strip())
            else:
                감소대책_str = item.감소대책.strip()

            table.add_row(
                str(item.번호),
                item.설비,
                item.물질,
                item.유해위험요인_분류,
                item.유해위험요인,
                item.관련근거,
                item.위험_가능성,
                item.위험_중대성,
                item.위험성,
                감소대책_str
            )

        console.print(table)

    # 기타 정보 출력
    if isinstance(기타, str):
        etc = Table(show_header=True, header_style="bold yellow")
        etc.add_column("기타 사항", justify="left")
        etc.add_row(기타)
        console.print(etc)

    elif isinstance(기타, list):
        etc = Table(show_header=True, header_style="bold yellow")
        etc.add_column("기타 사항", justify="left")
        for item in 기타:
            etc.add_row(f"- {item}")
        console.print(etc)

__all__ = ["pretty_print_risk_evaluation"]
